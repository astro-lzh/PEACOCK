# Getting started

Run a C II simulation and turn its escaping photons into a spectrum. The same
configuration and clump catalogue work on the CPU and on an NVIDIA GPU.

(installation-source)=

(installation-dependencies)=
## 1. Install PEACOCK and open the source folder

Download and extract the [source archive](download.md). In your terminal, change into
the extracted `PEACOCK` directory containing `peacock.py`. If you are in its parent
directory, use `cd PEACOCK`. Follow the [installation instructions](installation.md)
for your operating system, including the CUDA dependencies for a GPU run.

On Linux and macOS, keep that environment active when using `python3`. In Windows
PowerShell, use `.\.venv\Scripts\python.exe` in place of `python3`; complete Windows
commands for both backends are included below.

## 2. Choose a spectral line

List the available line identifiers:

```bash
python3 peacock.py lines
```

This tutorial uses `CII1334`. It includes the coupled C II 1334/1335 transitions and uses
C II 1334.53 Å as the reference wavelength. Selecting a line loads its atomic data and
scattering rules. You can reuse a backend build when selecting another supported line.

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

## 4. Make the spectrum

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

With 100,000 photons and a 150 km s⁻¹ radial outflow, the deepest C II absorption is centered at −150 km s⁻¹, where the flux falls to 0.635 of the incident continuum. The shaded band shows approximate Monte Carlo sampling uncertainty.
```

Independent runs sample different photon paths. When comparing CPU and GPU spectra, use
the same bins and aperture and compare any difference with the sampling uncertainties.
The [output guide](outputs.md) explains the packet files, normalization and aperture.

(installation-settings)=
## 5. Change the physical model

Copy `examples/cii/quickstart.cfg` to `my-cii.cfg` and edit the copy. These are the main
settings in this example; lengths in the configuration are in parsecs.

| Physical setting | Configuration entry | Example value | Unit |
| --- | --- | --- | --- |
| Launched photons | `[run] nphot` | `100000` | Count |
| Inner and outer clump placement bounds | `[grid] cloud_rin`, `cloud_rout` | `(100)`, `(950)` | pc |
| Clump radius | `[cloud1] size`, `rmax` | `50`, `50` | pc |
| Clump volume filling factor | `[grid] cloud_filling_factors` | `(0.1)` | Dimensionless |
| Clump gas temperature | `[cloud1] temperature` | `10000` | K |
| C II reference lower-level column across one clump radius | `[cloud1] hydrogen` | `c 3e15` | cm⁻² |
| Random velocity dispersion and radial outflow | `[grid] cloud_motion_params` | `((25,150,0,0,0,0))` | km s⁻¹ for the first two entries |
| Excited-to-ground lower-level population ratio | `[emission] cii_ratio_21` | `0.3` | Dimensionless |
| Injected continuum velocity half-width | `[emission] frequency_param` | `600` | km s⁻¹ |

The motion setting `cloud_motion_modes = ((2,1))` combines a Gaussian random velocity
with a constant radial outflow. The first two motion parameters therefore mean
25 km s⁻¹ dispersion in each Cartesian component and 150 km s⁻¹ outward speed. For this
C II configuration, `hydrogen = c 3e15` sets the C II column in the reference lower level.
The source uses `frequency_mode = 3`, so its continuum spans −600 to +600 km s⁻¹.
The inner placement bound applies to clump centers, while complete clumps fit within the
outer bound. The input column is density times one clump radius; the column through a
clump diameter is twice this value.

The supplied catalogue fixes the clump positions. If you change the clump radius, shell
boundaries or filling factor, prepare a matching complete catalogue as described in the
source folder's `docs/cloud-model.md`. The [physical model](models.md) explains what
these quantities mean.

Run the edited configuration with the same catalogue when its geometry is unchanged:

```bash
python3 peacock.py run --line CII1334 --backend cpu --config my-cii.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/my-cii
python3 tools/plot_spectrum.py run/my-cii --output run/my-cii/spectrum.png
```

For a GPU run, select `--backend cuda` and choose a different output directory.
The optional `--nphot` argument overrides the packet count in the configuration.

## Keep a run reproducible

The example fixes `[grid] random_seed` for the gas realization and `[run] random_seed`
for photon sampling. Keep the geometry seed and catalogue fixed when comparing two
independent transport calculations, and change the photon seed between them. Keep each
run's resolved configuration, atomic table, packet output and run summary together.

Next, [inspect the outputs](outputs.md), [explore the examples](examples.md), or use
[troubleshooting](troubleshooting.md) if a command fails.
