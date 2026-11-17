"""Fit the J1253-0312 C II spectrum, replay the archived fit or bin photon packets."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np


def apply_observation(fine, data):
    """Apply the same window normalization, velocity shift, pixel bins and scale."""
    area = np.einsum("...i,i->...", fine, data["normalization_weights"])
    if np.any(~np.isfinite(area) | (area <= 0)):
        raise ValueError("The normalization window has no positive flux.")
    fine = fine / np.expand_dims(area, -1)
    native = data["flux_scale"] * np.einsum("...i,ji->...j", fine, data["rebin_matrix"])
    return fine, native


def predict(theta, data):
    """Map [A, q, log10(N1)] to the flux density on the observed pixel grid."""
    features = np.array(theta, dtype=float, copy=True)
    features[..., 0] = np.log10(features[..., 0])
    h = (features - data["xmean"]) / data["xscale"]
    layers = int(data["n_layers"])
    for i in range(layers):
        h = np.einsum("...i,ij->...j", h, data[f"w{i}"]) + data[f"b{i}"]
        if i < layers - 1:
            h = np.maximum(h, 0.0)
    fine = np.maximum(h * data["yscale"] + data["ymean"], 1e-12)
    return apply_observation(fine, data)[1]


def prior_transform(unit):
    """Independent uniform priors in log10(A), q and log10(N1)."""
    return np.array([9.0**unit[0], 1.0 + 2.0 * unit[1], 14.3 + unit[2]])


def new_fit(data, output, seed, nlive, dlogz):
    import dynesty
    import matplotlib

    matplotlib.use("Agg")
    from dynesty import plotting, utils
    from matplotlib import pyplot as plt

    if output.exists():
        raise FileExistsError(f"Choose a new output directory for this fit: {output}")
    if nlive < 4 or not np.isfinite(dlogz) or dlogz <= 0:
        raise ValueError("Use at least four live points and a positive finite dlogz.")

    # Cache the arrays once so each likelihood call evaluates only the network.
    data = dict(data)
    observed = data["observed"]
    variance = data["likelihood_variance"]
    normalization = np.log(2 * np.pi * variance).sum()

    def loglike(theta):
        residual = observed - predict(theta, data)
        return -0.5 * (np.sum(residual**2 / variance) + normalization)

    sampler = dynesty.NestedSampler(loglike, prior_transform, ndim=3, nlive=nlive,
                                    bound="multi", sample="rwalk",
                                    rstate=np.random.default_rng(seed))
    sampler.run_nested(dlogz=dlogz, print_progress=False)
    results = sampler.results
    weights = results.importance_weights()
    names = ("A", "q", "log10_N1")
    levels = (0.16, 0.50, 0.84)
    quantiles = {}
    for name, samples in zip(names, results.samples.T):
        p16, median, p84 = utils.quantile(samples, levels, weights=weights)
        quantiles[name] = {"p16": float(p16), "median": float(median), "p84": float(p84)}
    summary = {
        "dynesty_version": dynesty.__version__, "seed": seed, "nlive": nlive,
        "dlogz": dlogz, "bound": "multi", "sample": "rwalk",
        "likelihood_calls": int(np.sum(results.ncall)), "samples": len(weights),
        "effective_samples": float(1.0 / np.sum(weights**2)),
        "parameters": quantiles,
    }
    labels = [r"$A$ [$\mathrm{kpc}^{-1}$]", r"$q$",
              r"$\log_{10}(N_1/\mathrm{cm}^{-2})$"]
    fig, _ = plotting.cornerplot(
        results, labels=labels, color="#176776", span=[0.999] * 3,
        quantiles=levels, quantiles_2d=[0.68, 0.95], show_titles=True,
        title_quantiles=levels, title_fmt=".2f", title_kwargs={"fontsize": 10},
        max_n_ticks=4,
        hist2d_kwargs={"plot_datapoints": False},
    )
    fig.subplots_adjust(hspace=0.14, wspace=0.10)
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as temp:
        staged = Path(temp) / "fit"
        staged.mkdir()
        fig.savefig(staged / "corner.png", dpi=160, bbox_inches="tight")
        plt.close(fig)
        np.savez_compressed(staged / "posterior.npz", parameter_names=names,
                            samples=results.samples, weights=weights,
                            logl=results.logl, logwt=results.logwt)
        (staged / "summary.json").write_text(json.dumps(summary, indent=2) + "\n",
                                             encoding="utf-8")
        staged.rename(output)
    for name, values in quantiles.items():
        print(f"{name}: {values['median']:.4f} [{values['p16']:.4f}, {values['p84']:.4f}]")
    print(f"Saved posterior.npz, summary.json and corner.png in {output}")


def replay(data, output):
    # Re-score the candidate samples from the archived nested fit.
    theta = data["posterior_candidates"]
    model = predict(theta, data)
    variance = data["likelihood_variance"]
    observed = data["observed"]
    chi2 = np.sum((observed - model)**2 / variance, axis=-1)
    best = int(np.argmin(chi2))
    np.testing.assert_array_equal(theta[best], data["rt_parameters"])
    prediction = model[best]
    np.testing.assert_allclose(prediction, data["reference_prediction"], rtol=5e-11, atol=1e-14)

    # Both direct calculations use theta[best] and distinct packet seeds.
    rt = data["rt_spectra"]
    rt_mean = rt.mean(axis=0)
    rt_mean_covariance = data["rt_covariances"].sum(axis=0) / len(rt)**2
    rt_sigma = np.sqrt(np.diag(rt_mean_covariance))
    residual = rt_mean - prediction
    rms = np.sqrt(np.mean(residual**2))
    valid = rt_sigma > 0
    rms_in_mc_sigma = np.sqrt(np.mean((residual[valid] / rt_sigma[valid])**2))

    print(f"Candidate samples: {len(theta)}")
    print(f"Best A={theta[best, 0]:.6f} kpc^-1, q={theta[best, 1]:.6f}, "
          f"log10(N1/cm^-2)={theta[best, 2]:.6f}")
    print(f"Chi-square: {chi2[best]:.6f} on {len(observed)} observed pixels")
    print("Independent transport seeds:", *data["rt_transport_seeds"])
    print(f"RT minus DNN RMS: {rms:.8g}; {rms_in_mc_sigma:.3f} in per-pixel MC sigma")
    if output is not None:
        np.savetxt(output, np.column_stack([
            data["observed_velocity"], observed, data["observed_sigma"], prediction,
            rt[0], rt[1], rt_mean, rt_sigma, residual,
        ]), delimiter=",", comments="", header=(
            "velocity_km_s,observed,observed_sigma,dnn,rt1,rt2,"
            "rt_mean,rt_mean_mc_sigma,rt_minus_dnn"
        ))


def bin_packets(data, packet_path, output):
    if packet_path.is_dir():
        paths = list(packet_path.glob("packets_*.dat"))
        if len(paths) != 1:
            raise ValueError("Expected one primary ASCII packet file in the run directory.")
        packet_path = paths[0]
    # ASCII_LYA has global position, direction, observer detuning and Doppler width.
    packets = np.loadtxt(packet_path, usecols=(0, 1, 2, 3, 4, 5, 6, 8), ndmin=2)
    if not len(packets):
        raise ValueError("No escaping packets in the ASCII file.")
    position = packets[:, :3]
    direction = packets[:, 3:6]
    direction = direction / np.linalg.norm(direction, axis=1)[:, None]
    impact_pc = np.linalg.norm(np.cross(position, direction), axis=1) / 3.08567758e18
    select = (impact_pc > 0) & (impact_pc <= float(data["aperture_pc"]))
    # C II ASCII x is already in the observer frame. Positive velocity is red.
    velocity = -299792.458 * packets[:, 6] * packets[:, 7] / float(data["reference_hz"])
    counts = np.histogram(velocity[select], bins=data["fine_edges"])[0]
    fine, native = apply_observation(counts, data)
    np.savez_compressed(output, counts=counts, fine=fine, native=native)
    print(f"{counts.sum()} packets in {len(counts)} fine bins, "
          f"rebinned to {len(native)} observed pixels")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    archived = sub.add_parser("replay", help="Re-score the saved candidates and compare independent RT")
    archived.add_argument("data", type=Path)
    archived.add_argument("--output", type=Path)
    fit = sub.add_parser("fit", help="Sample a fresh posterior with the saved DNN and observed spectrum")
    fit.add_argument("data", type=Path)
    fit.add_argument("--output", type=Path, required=True, help="New directory for fit results")
    fit.add_argument("--seed", type=int, default=17, help="Nested-sampling random seed")
    fit.add_argument("--nlive", type=int, default=300, help="Number of live points")
    fit.add_argument("--dlogz", type=float, default=0.05, help="Evidence-based stopping threshold")
    bins = sub.add_parser("bin", help="Make one spectrum from C II ASCII escape packets")
    bins.add_argument("data", type=Path)
    bins.add_argument("packets", type=Path, help="An ASCII packet file or its run directory")
    bins.add_argument("output", type=Path)
    args = parser.parse_args()
    with np.load(args.data, allow_pickle=False) as data:
        if args.command == "replay":
            replay(data, args.output)
        elif args.command == "fit":
            new_fit(data, args.output, args.seed, args.nlive, args.dlogz)
        else:
            bin_packets(data, args.packets, args.output)


if __name__ == "__main__":
    main()
