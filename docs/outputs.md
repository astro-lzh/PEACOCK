# Spectra and output files

## Read a spectrum in Python

To find the deepest part of the C II absorption line, open the `spectrum.csv`
from the [C II tutorial](getting-started.md). Each row gives the flux in one
velocity interval. The companion file, `spectrum.json`, tells you which transition
sets zero velocity, how the flux was normalized and which aperture was used.
Run the example from the PEACOCK source folder.

```python
import json
from pathlib import Path

import numpy as np

run = Path("run/cii")  # Use run/cii-cuda for the GPU tutorial.
spectrum = np.genfromtxt(run / "spectrum.csv", delimiter=",", names=True, ndmin=1)
settings = json.loads((run / "spectrum.json").read_text(encoding="utf-8"))

print(settings["line_label"], settings["normalization"])
print(f"{len(spectrum)} bins, {int(spectrum['escaped_packets'].sum()):,} packets in range")
deepest = spectrum[np.argmin(spectrum["flux"])]
print(f"Lowest flux: {deepest['flux']:.3f} at {deepest['velocity_km_s']:.0f} km/s")
```

The strongest absorption in the CPU tutorial is on the blue side of the line.
At −150 km/s the flux is 0.695 times the incident continuum. All 100,000 packets
fall within the 60 plotted bins.

| CSV column | Unit | Meaning |
| --- | --- | --- |
| `velocity_km_s` | km/s | Bin center relative to the reference transition. Positive velocities are redward. |
| `flux` | Dimensionless for `continuum`, (km/s)⁻¹ for `probability` | Flux relative to the injected continuum, or probability density per unit velocity. A probability-normalized profile has unit area across the plotted bins. |
| `mc_sigma` | Same as `flux` | Approximate Monte Carlo uncertainty for that bin, using the square root of its packet count and the same normalization as the flux. |
| `escaped_packets` | packets | Escaped packets in this bin that pass the aperture cut. |
| `bin_left_km_s` | km/s | Lower velocity edge of the bin. |
| `bin_right_km_s` | km/s | Upper velocity edge of the bin. |

You can use the three counts in `spectrum.json` to follow the selection. Start
with all photons that escaped the wind (`escaped_packets`), keep those within
the aperture (`aperture_packets`), then count those inside the plotted velocity
range (`binned_packets`). This last count equals the sum of the CSV packet
counts. For example, the [250 pc aperture](choosing-a-line-and-an-observable.md#how-aperture-size-affects-the-c-ii-line-profile)
selects 98,202 of the 100,000 escaped CPU photons. All of the selected photons
fall inside the plotted velocity range of −600 to +600 km/s.

## Read individual photon packets

The spectrum combines photons by velocity. To see which photons scattered or which
rays enter a smaller aperture, start with the packet file named in `spectrum.json`.
The CPU tutorial writes one row per escaped photon. The CUDA archive stores every
launched photon, with `status == 1` marking an escape.

| Quantity | CPU ASCII (columns start at 1) | GPU packet archive | Unit |
| --- | --- | --- | --- |
| Number of scatterings before escape | `nscatter` (13) | `nscatter` for `status == 1` | count |
| Position on the escaping ray | `pos` (1–3), at the last scattering or at emission for a direct photon | `pos0`, `pos1`, `pos2`, at the end of the ray | cm |
| Outgoing direction | `dir` (4–6) | `dir0`, `dir1`, `dir2` | dimensionless |
| Distance traveled since the last scattering (or emission for a direct photon) | `dist` (12) | `dist` | cm |
| Frequency offset | `x` (7), observer frame | `x`, local frame, with `sc_dir_bulk` giving the projected bulk-motion correction | Doppler widths (dimensionless) |
| Doppler width | `Delta_nu_D` (9) | `Delta_nu_D` | Hz |

### Count escaped C II photons that scattered

After plotting the [C II tutorial](getting-started.md), run the following Python code
from the PEACOCK source folder. Set `run` to the directory you produced. The bundled
GPU reader selects escaped rays and converts their frequencies using the run's atomic
table. Use the same escape selection for the scattering counts so all arrays describe
the same photons in the same order.

```python
import json
from pathlib import Path

import numpy as np
from tools.plot_spectrum import cuda_packets, load_atom, selected_profile

run = Path("run/cii")  # Use run/cii-cuda for a GPU calculation.
settings = json.loads((run / "spectrum.json").read_text(encoding="utf-8"))
nu0 = settings["reference_frequency_hz"]
if settings["backend"] == "cpu":
    packets = np.loadtxt(run / settings["packet_file"], ndmin=2)
    position_cm, direction = packets[:, :3], packets[:, 3:6]
    frequency_hz = nu0 + packets[:, 6] * packets[:, 8]
    nscatter = packets[:, 12].astype(int)
else:
    atom = load_atom(selected_profile(run, settings), run / "atomic.atom")
    frequency_hz, position_cm, direction, path, _ = cuda_packets(run, atom)
    with np.load(path, allow_pickle=False) as packets:
        escaped = packets["status"] == 1
        nscatter = packets["nscatter"][escaped]

scattered = nscatter > 0
print(f"{scattered.sum():,} scattered out of {nscatter.size:,} escaped")
```

About three in every hundred photons scattered before they escaped in the C II
tutorial. The table gives the counts for a wind moving outward at 150 km/s.

| Photon count or fraction | CPU | NVIDIA RTX 5090 |
| --- | ---: | ---: |
| All escaped photons | 100,000 | 100,000 |
| Escaped without scattering | 97,136 | 97,107 |
| Escaped after at least one scattering | 2,864 | 2,893 |
| Fraction of escaped photons that scattered | 2.864% | 2.893% |

Both runs sampled the same wind. Individual photon paths vary with Monte Carlo
sampling. A photon that scatters several times contributes once to the scattered count.
The [four-panel C II example](examples.md#photon-scattering-statistics) shows how to
use the same records to find the distribution of last scattering radii.

### Observing aperture

A circular aperture selects escaping rays by their **projected distance** from the
halo center. A photon can scatter far from the center in three dimensions and still
travel along a ray that passes close to the center on the sky. For a point
$\boldsymbol r$ on that ray and its unit direction $\hat{\boldsymbol n}$, the
projected distance is $b=|\boldsymbol r\times\hat{\boldsymbol n}|$. It is the same
at the last scattering and at the halo boundary. Continue with the arrays above to
count the rays that enter a projected aperture of radius 250 pc.

```python
from tools.plot_spectrum import PC_CM

unit_direction = direction / np.linalg.norm(direction, axis=1)[:, None]
impact_pc = np.linalg.norm(np.cross(position_cm, unit_direction), axis=1) / PC_CM
in_aperture = impact_pc <= 250
print(f"{in_aperture.sum():,} escapes in the aperture, including "
      f"{(in_aperture & scattered).sum():,} that scattered")
```

Of the 100,000 escapes in each tutorial run, the 250 pc aperture selects 98,202
CPU packets (1,066 scattered) and 98,178 GPU packets (1,071 scattered).
Omitting this cut gives the full-aperture spectrum. Both
selections average over all outgoing directions. A smaller aperture can remove
extended scattered light while retaining the compact continuum source, as in the
{ref}`C II aperture comparison <cii-aperture-comparison>`. For a model-to-data
comparison, match the observational aperture as in the {ref}`C II fitting walkthrough
<dnn-tutorial>`.

### Frequency and velocity

To place a photon on the spectrum, compare its frequency as seen by the observer
with the rest frequency of the reference transition. The CPU ASCII column `x`
gives this offset in units of the packet's Doppler width. Its frequency in Hz is
$\nu_{\rm obs}=\nu_0+x\,\Delta\nu_D$.
For the tutorial's CUDA C II archive, the reader adds `sc_dir_bulk` to the local `x`
before multiplying by `Delta_nu_D` and adding $\nu_0$. For other GPU lines it uses
`nu_final_Hz` when available or applies the frame conversion for that atomic network.

To compare these photons with the plotted spectrum, use the same reference transition
and the same redward-positive convention, $v=-c(\nu_{\rm obs}-\nu_0)/\nu_0$.
For C II, zero velocity corresponds to 1334.53 Å. Photons from the coupled
fine-structure transitions are plotted relative to that same wavelength. The array
below gives one velocity per escaped photon, in km/s. The CSV reports the centers
of the velocity bins.

```python
from tools.plot_spectrum import C_KMS

velocity_km_s = -C_KMS * (frequency_hz - nu0) / nu0
counts, edges = np.histogram(velocity_km_s[in_aperture], bins=settings["bins"],
                             range=settings["velocity_range_km_s"])
```

`counts` now contains the packet counts per velocity bin for that aperture. To make
the same selection with the command-line plotter, add `--aperture-pc 250` and use the
same bin edges and normalization on either backend.

## Plot a completed run

To generate the figure, CSV and JSON for a run, give the plotting tool the run directory
and an output filename.

```bash
python3 tools/plot_spectrum.py run/cii --output run/cii/spectrum.png
```

The figure, table and settings share the same filename stem. For example, choosing
`spectrum-aperture.png` produces `spectrum-aperture.csv` and `spectrum-aperture.json`
alongside the figure.

## Which files should I keep?

| File | Meaning |
| --- | --- |
| `resolved.cfg` | The configuration actually supplied to the transport engine, including the chosen output paths and packet count. |
| `atomic.atom` | The atomic network used by this run, including its reference transition. |
| `packets_*.dat` | Escaped-photon ASCII output from the CPU example. Comment lines describe the columns. |
| `run.json` | CPU run summary identifying the selected line, packet count, photon seed and inputs. |
| `gpu_output_*.npz` | CUDA packet arrays, including the final status of every launched packet. |
| `gpu_run_report.json` | CUDA run summary, including escaped, absorbed and incomplete packet counts. |
| `prepare_report.json` | Record of the prepared CUDA inputs. |
| `spectrum.png`, `spectrum.csv`, `spectrum.json` | The plotted spectrum, its binned data and the plotting settings. |

Keep the complete run directory. For a calculation using an external clump catalogue,
also retain that catalogue. Record the PEACOCK release and the settings used to turn the
packets into a spectrum.

## Escaping and absorbed photons

The plotting tool selects escaped packets automatically. The CUDA run summary reports
escapes, physical absorption and unfinished histories separately. Resolve any unfinished
histories before interpreting the spectrum.

If all photons are physically absorbed, a continuum-normalized spectrum has zero flux.
A probability-normalized shape requires at least one escaped packet inside the selected
aperture and velocity range.

## Continuum normalization and bin width

In the C II tutorial, a flux of one is the level expected from the source
continuum before its light passes through the wind. The source emits equal-weight
photons uniformly from −600 to +600 km s⁻¹. Within that window, the expected
continuum count in each bin is the total number launched times the fraction of
the velocity window covered by the bin. The plotter divides the escaping count
by that expected count. You can then see how much the wind and the observing
aperture change the flux.

The default plot divides the continuum window into 60 bins. For narrower bins
and a smaller aperture, run the plotter again on the same output.

```bash
python3 tools/plot_spectrum.py run/cii --bins 120 --velocity-range -600 600 --aperture-pc 250 --output run/cii/spectrum-aperture.png
```

Narrow bins resolve finer features but contain fewer packets each. The
`mc_sigma` column estimates the resulting sampling noise from the square root
of each bin's count, scaled to the same continuum. More photons reduce the
noise. When comparing weak features, use the same velocity edges and normalization
for both spectra.

### Intrinsic line sources

A Gaussian line source has a different incident spectrum from the flat-continuum
example. Use `--normalization probability` to display its escaped spectral shape:

```bash
python3 tools/plot_spectrum.py run/lya --normalization probability --output run/lya/spectrum.png
```

This gives unit area among the accepted photons in the plotted velocity range. It does
not measure the escape fraction. Preserve the input line-to-continuum ratio and the
source normalization when combining separately simulated emission components.
For a line source the default plotting window is −600 to +600 km s⁻¹; use
`--velocity-range` to include wider scattered wings when needed.
