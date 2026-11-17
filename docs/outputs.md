# Spectra and output files

A PEACOCK run follows photon packets through the gas and records their outcomes. To make
a spectrum, select the packets that escaped, apply an observing aperture if needed, and
count their frequencies in bins. The plotting tool performs these steps for both CPU and
CUDA runs.

## Plot a completed run

From the source folder, run:

```bash
python3 tools/plot_spectrum.py run/cii --output run/cii/spectrum.png
```

Replace `run/cii` with the directory created by your simulation. The tool reads the run's
line and atomic data, writes the figure to `spectrum.png`, and saves the binned spectrum
beside it as `spectrum.csv`. A third file, `spectrum.json`, records the line, binning,
aperture and normalization used to make the plot.

CPU plotting uses the ASCII escape-packet output selected by the quick-start
configuration. CUDA plotting reads the packet archive named by the run summary.
The CSV columns give velocity, flux, approximate Monte Carlo uncertainty, escaping
packet count, and the left and right velocity-bin edges.

The [C II tutorial](getting-started.md) supplies a complete example using the same
configuration on the CPU and GPU.

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

The CPU example's ASCII spectrum file contains escaped packets. CUDA output contains all
launched packets; use `status == 1` for those that escaped. Physically absorbed photons
and incomplete or numerically failed histories do not contribute to the escaping
spectrum. The CUDA summary reports these outcomes separately.

The plotting tool selects escaped packets automatically. Check the run summary before
interpreting a spectrum: unfinished histories require attention because they are not
physical absorption.

If all photons are physically absorbed, a continuum-normalized spectrum has zero flux.
A probability-normalized shape requires at least one escaped packet inside the selected
aperture and velocity range.

## Frequency and velocity

Every line selection has a reference transition. For the C II example the zero point is
C II 1334.53 Å, and all coupled branches use this same velocity axis. Their wavelength
separation therefore appears as an offset in the plotted spectrum.

The plotted velocity is redward-positive: a photon at a longer wavelength than the
reference has positive velocity, and a bluer photon has negative velocity. The tool uses
$v=-c(\nu_{\mathrm{obs}}-\nu_0)/\nu_0$ for both CPU and CUDA outputs, where $\nu_0$ is the
selected reference frequency. Raw dimensionless detuning is measured in Doppler widths,
so it must first be converted using the packet's Doppler width and observer-frame
frequency.

Use the same reference transition and velocity convention when comparing the result with
observations or another run.

## Continuum normalization and bin width

The quick-start C II model injects equal-weight photons uniformly from −600 to
+600 km s⁻¹. For a velocity bin inside this window, the incident continuum would supply
the launched packet count multiplied by the bin width and divided by the full source
width. Dividing the escaping count by that incident count gives a continuum-normalized
spectrum with an incident level of one.

This normalization retains attenuation and the effect of the aperture. The plotting tool
also gives an approximate Monte Carlo uncertainty from the square root of the escaping
count in each bin. More photons reduce this sampling noise.

The default is 60 bins spanning the injected continuum window, which is −600 to
+600 km s⁻¹ for the quick-start case. For example, to use a smaller aperture and finer
velocity bins:

```bash
python3 tools/plot_spectrum.py run/cii --bins 120 --velocity-range -600 600 --aperture-pc 250 --output run/cii/spectrum-aperture.png
```

Narrow bins resolve finer features but contain fewer packets. Compare spectra on the
same velocity edges and with the same normalization, and increase the packet count when
a result depends on a weak feature.

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

## Observing aperture

An aperture selects escaping rays by projected distance from the halo center. For a ray
with position $\boldsymbol r$ and unit direction $\hat{\boldsymbol n}$, its impact
parameter is $b=|\boldsymbol r\times\hat{\boldsymbol n}|$.

The standard plot combines escaping photons across directions to represent the unresolved,
all-sky spectrum. Without `--aperture-pc`, it includes all escaping packets. Supply an
aperture radius in parsecs to select a smaller projected region. Use the same physical
aperture when comparing models with an observed spectrum. A smaller aperture can remove
extended scattered emission while retaining the compact continuum source.
The {ref}`C II aperture comparison <cii-aperture-comparison>`
shows this effect using two spectra extracted from the same run.

The {ref}`C II fitting walkthrough <dnn-tutorial>` shows a separate example with an
explicit observational aperture and pixel grid. Its normalization and observation mapping
are part of that particular fit.
