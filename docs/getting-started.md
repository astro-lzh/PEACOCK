(getting-started)=
# Run your first C II simulation

Use PEACOCK to follow photons through a clumpy wind and plot the C II spectrum
that emerges. Choose a CPU or an NVIDIA GPU. Both use the same cloud catalogue,
model configuration and plotting tool.

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

This tutorial uses `CII1334`. It includes the coupled C II 1334/1335 transitions and uses
C II 1334.53 Å as the reference wavelength. Selecting a line loads its atomic data and
scattering rules. You can reuse a backend build when selecting another supported line.
See [Choosing a line and an observable](choosing-a-line-and-an-observable.md) for the
transitions included in each selection.

(installation-first-run)=
## 3. Run the C II example

The example launches 100,000 continuum photons through 685 gas clumps. Each clump moves
outward at 150 km s⁻¹ and also has a random velocity with a dispersion of 25 km s⁻¹
per Cartesian component. The C II selector loads the same `examples/cii/quickstart.cfg`
and `examples/cii/quickstart-clumps.txt` on either backend.

Choose the commands for your backend and operating system. Build once for each backend.
For subsequent simulations, reuse that build and give each run a new output directory.

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

Use the command for the operating system and backend you used to run the simulation.

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

Open `spectrum.png` to see the C II profile. The accompanying `spectrum.csv` contains the
binned values for your own analysis, and `spectrum.json` records the plotting settings.
Velocity is measured relative to C II 1334.53 Å. Negative velocity is blueward and positive
velocity is redward. The plot uses the injected flat continuum to set a continuum level
of one.

```{figure} assets/research/cii-100k-v150-spectrum.png
:alt: C II spectrum from the tutorial run, with velocity on the horizontal axis and flux relative to the injected continuum on the vertical axis.
:width: 100%

With 100,000 photons and a 150 km s⁻¹ radial outflow, the reference CPU run has its deepest absorption at −150 km s⁻¹. The flux in this bin is 0.635 of the incident continuum. The shaded band shows approximate Monte Carlo sampling uncertainty.
```

{download}`Download the reference spectrum with flux, packet counts and sampling uncertainties (CSV) <assets/research/cii-100k-v150-spectrum.csv>`

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

The example fixes `[grid] random_seed` for the gas realization and `[run] random_seed`
for photon sampling. Keep the geometry seed and catalogue fixed when comparing two
independent transport calculations, and change the photon seed between them. Keep each
run's resolved configuration, atomic table, packet output and run summary together.

Next, [choose a line and an observable](choosing-a-line-and-an-observable.md) to
model a different transition or measure the spectrum through a smaller aperture.
