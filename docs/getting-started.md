(getting-started)=
(run-your-first-c-ii-simulation)=
# Run your first PEACOCK simulation

Choose a spectral line, follow photons through a clumpy wind and plot the
spectrum that emerges. This tutorial uses C II as an example. You can run it
on a CPU or an NVIDIA GPU with the same wind configuration, clump catalogue
and plotting tool.

(installation-source)=
(installation-dependencies)=
(install-peacock-and-open-the-source-folder)=
## 1. Open the source folder

Start in the extracted `PEACOCK` directory containing `peacock.py`, with the environment
from [Download and install](installation.md). On Linux or macOS, activate it with
`. .venv/bin/activate`. The Windows PowerShell commands below call the environment's
Python directly.

## 2. Choose a spectral line

List the available line identifiers:

```bash
python3 peacock.py lines
```

In Windows PowerShell, use `.\.venv\Scripts\python.exe peacock.py lines`.

For this example, choose `CII1334` to follow the C II transitions near 1334 and 1335 Å together.
PEACOCK loads their atomic data and scattering rules for you. Once you have built the
CPU or GPU program, you can use the same program to [run another supported line](choosing-a-line-and-an-observable.md).

(installation-first-run)=
## 3. Run the C II example

The source shines a flat continuum through a wind. The gas clumps move outward
at 150 km/s, with random motion superimposed. The simulation follows 100,000
photons to determine how the wind reshapes that continuum.

Choose the commands for your processor and operating system. The first command
builds PEACOCK. The second runs the model. For later simulations, reuse the build
and choose a fresh output directory.

### CPU

On Linux or macOS, run

```bash
python3 peacock.py build --backend cpu
python3 peacock.py run --line CII1334 --backend cpu --output run/cii
```

In Windows PowerShell, use the location of your UCRT64 installation.

```powershell
.\.venv\Scripts\python.exe peacock.py build --backend cpu --compiler-prefix C:/msys64/ucrt64
.\.venv\Scripts\python.exe peacock.py run --line CII1334 --backend cpu --output run/cii
```

### NVIDIA GPU

The build command below targets an RTX 5090. If you have a different card, look up
its [GPU target](gpu.md#choose-your-gpu-target) and replace `compute_120`. The run
command prepares the cloud grid and photon inputs, then transports the photons on the GPU.

On Linux, run

```bash
python3 peacock.py build --backend cuda --arch compute_120
python3 peacock.py run --line CII1334 --backend cuda --output run/cii-cuda
```

In Windows PowerShell, set `$ucrt` to the directory containing your UCRT64 toolchain.
The command uses the Clang C++ compiler installed in the [Windows setup](installation.md#windows).

```powershell
$ucrt = "C:/msys64/ucrt64"
.\.venv\Scripts\python.exe peacock.py build --backend cuda --arch compute_120 --compiler-prefix "$ucrt" --cxx "$ucrt/bin/clang++.exe"
.\.venv\Scripts\python.exe peacock.py run --line CII1334 --backend cuda --output run/cii-cuda
```

(tutorial-spectrum)=
## 4. Make the spectrum

Choose the plotting command for the system and processor you used in step 3.

For a CPU run, use

```bash
python3 tools/plot_spectrum.py run/cii --output run/cii/spectrum.png
```

For a GPU run, use

```bash
python3 tools/plot_spectrum.py run/cii-cuda --output run/cii-cuda/spectrum.png
```

For a CPU run in Windows PowerShell, use

```powershell
.\.venv\Scripts\python.exe tools/plot_spectrum.py run/cii --output run/cii/spectrum.png
```

For a GPU run in Windows PowerShell, use

```powershell
.\.venv\Scripts\python.exe tools/plot_spectrum.py run/cii-cuda --output run/cii-cuda/spectrum.png
```

Open `spectrum.png` and look for the absorption trough on the blue side of the
line. A flux of one marks the incident continuum. The horizontal axis measures
velocity relative to C II 1334.53 Å, with blueshift to the left and redshift to
the right. The accompanying `spectrum.csv` gives the values in each velocity bin,
and `spectrum.json` records how they were plotted.

```{figure} assets/research/cii-100k-v150-spectrum-ymin06.png
:name: cii-tutorial-spectrum
:alt: C II tutorial spectrum with the flux axis starting at 0.6. The blue absorption trough reaches about 0.70 near −150 km/s.
:width: 100%

The deepest absorption in the CPU run is near −150 km/s, where the flux is about
70% of the incident continuum. Each clump has a center-to-edge ground-level C II
column of $5\times10^{14}\,\mathrm{cm}^{-2}$ and $n_2/n_1=0.1$. The shaded band
shows the approximate uncertainty from sampling a finite number of photons.
```

{download}`Download the reference spectrum with flux, packet counts and sampling uncertainties (CSV) <assets/research/cii-100k-v150-spectrum.csv>`

```{raw} html
<details><summary>Set the lower flux limit to 0.6 in your own plot</summary>
```

The 1.0.4 plotting command starts the flux axis at zero. To reproduce the
close-up above, run this Python example from the source directory after making
`spectrum.csv`. It saves `spectrum-zoom.png` in your run directory.

```python
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

run = Path("run/cii")  # Use "run/cii-cuda" for the GPU example.
s = np.genfromtxt(run / "spectrum.csv", delimiter=",", names=True)
edges = np.r_[s["bin_left_km_s"], s["bin_right_km_s"][-1]]
fig, ax = plt.subplots(layout="constrained")
ax.stairs(s["flux"], edges, baseline=None, color="#176776")
ax.fill_between(s["velocity_km_s"], s["flux"] - s["mc_sigma"],
                s["flux"] + s["mc_sigma"], step="mid", color="#176776", alpha=0.15)
ax.axhline(1, color="gray", linestyle="--", linewidth=1)
ax.set(xlim=(edges[0], edges[-1]), ylim=(0.6, None),
       xlabel="Velocity relative to C II 1334.53 Å (km/s)", ylabel="Flux / injected continuum")
fig.savefig(run / "spectrum-zoom.png", dpi=180)
plt.close(fig)
```

```{raw} html
</details>
```

Independent runs sample different photon paths. When comparing CPU and GPU spectra, use
the same bins and aperture and compare any difference with the sampling uncertainties.
The [output guide](outputs.md) explains the packet files, normalization and aperture.

(installation-settings)=
## 5. Change the physical model

To try a faster wind, copy `examples/cii/quickstart.cfg` to `my-cii.cfg` in the
source directory. Under `[grid]`, change the second entry of `cloud_motion_params`
from `150` to `250` and save the file.

```ini
cloud_motion_params = ((25,250,0,0,0,0))
```

This keeps the random velocity dispersion at 25 km/s per Cartesian component and
increases the radial outflow to 250 km/s. Reuse the compiled program and original
clump catalogue, giving the new spectrum its own directory.

```bash
python3 peacock.py run --line CII1334 --backend cpu --config my-cii.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/my-cii
python3 tools/plot_spectrum.py run/my-cii --output run/my-cii/spectrum.png
```

For a GPU run, select `--backend cuda`. In Windows PowerShell, replace `python3` with
`.\.venv\Scripts\python.exe`. To double the photon count in a later run, add
`--nphot 200000` to the run command and use a new output directory.
[Configuring a PEACOCK simulation](configuring-a-peacock-simulation.md)
explains each input and shows how to replace the constant speed with an accelerating wind.

## Keep a run reproducible

To follow a new set of photon paths through the same wind, change
`[run] random_seed`. Keep the clump catalogue and `[grid] random_seed` fixed so
that the clump positions and velocities stay the same. Save the resolved configuration,
atomic table, packet output and run summary together.

Next, [choose a line and an observable](choosing-a-line-and-an-observable.md) to
model a different transition or measure the spectrum through a smaller aperture.
