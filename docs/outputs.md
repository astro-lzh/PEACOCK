# Spectra and output files

## Read a spectrum in Python

The [C II tutorial](getting-started.md) saves a spectrum with one row per velocity bin in
`spectrum.csv`. Open `spectrum.json` alongside it to see the reference transition,
normalization and aperture. Run this Python example from the PEACOCK source folder.

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

For the 100,000-photon CPU tutorial, the 60 bins contain 100,000 packets. The minimum
continuum-normalized flux is 0.635 in the bin centered at −150 km/s.

| CSV column | Unit | Meaning |
| --- | --- | --- |
| `velocity_km_s` | km/s | Bin center relative to the reference transition. Positive velocities are redward. |
| `flux` | Dimensionless for `continuum`, (km/s)⁻¹ for `probability` | Flux relative to the injected continuum, or probability density per unit velocity. A probability-normalized profile has unit area across the plotted bins. |
| `mc_sigma` | Same as `flux` | Approximate Monte Carlo uncertainty for that bin, using the square root of its packet count and the same normalization as the flux. |
| `escaped_packets` | packets | Escaped packets in this bin that pass the aperture cut. |
| `bin_left_km_s` | km/s | Lower velocity edge of the bin. |
| `bin_right_km_s` | km/s | Upper velocity edge of the bin. |

Summing the CSV packet counts gives `binned_packets` in the JSON file. The JSON also
records `escaped_packets` across the whole simulation and `aperture_packets` inside
the chosen aperture. In the [T15 accelerating wind example](configuring-a-peacock-simulation.md),
all 100,000 photons escaped, but one fell outside −600 to +600 km/s. The CSV counts
therefore sum to 99,999.

## Count escaped C II photons that scattered

How many photons interacted with the wind before they escaped? The binned spectrum
combines direct and scattered light. For the dust-free C II tutorial, use the individual
packet histories and count each escaped photon once if its `nscatter` is greater than
zero. These counts include all directions and velocities before any aperture cut.

**CPU.** Each row in the tutorial's ASCII packet file is an escaped photon. Its header
identifies `nscatter` as column 13, which is index 12 in Python.

```python
import json
from pathlib import Path

import numpy as np

run = Path("run/cii")
settings = json.loads((run / "spectrum.json").read_text(encoding="utf-8"))
nscatter = np.loadtxt(run / settings["packet_file"], usecols=12, dtype=int, ndmin=1)
print(f"{np.count_nonzero(nscatter > 0):,} scattered out of {nscatter.size:,} escaped")
```

**CUDA.** The packet archive contains every launched photon. Select the photons with
`status == 1` (escaped), then count those that scattered. The plotting step checks
that the run completed before writing `spectrum.json`, which names the packet file.

```python
import json
from pathlib import Path

import numpy as np

run = Path("run/cii-cuda")
settings = json.loads((run / "spectrum.json").read_text(encoding="utf-8"))
with np.load(run / settings["packet_file"], allow_pickle=False) as packets:
    escaped = packets["status"] == 1
    nscatter = packets["nscatter"][escaped]
print(f"{np.count_nonzero(nscatter > 0):,} scattered out of {nscatter.size:,} escaped")
```

The table compares the two 100,000-photon C II runs with the radial outflow set to 150 km/s.

| Photon count or fraction | CPU | NVIDIA RTX 5090 |
| --- | ---: | ---: |
| All escaped photons | 100,000 | 100,000 |
| Escaped without scattering | 95,632 | 95,690 |
| Escaped after at least one scattering | 4,368 | 4,310 |
| Fraction of escaped photons that scattered | 4.368% | 4.310% |

Both runs sampled the same wind. Individual photon paths vary with Monte Carlo
sampling. A photon that scatters several times contributes once to the scattered count.

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
