# Getting started

Install PEACOCK, build the transport engine, and simulate the spectral line you want to model.

(installation-source)=
## Obtain the source

Extract the [source archive](download.md) and open a terminal in the directory containing `peacock.py`.

(installation-dependencies)=
## CPU requirements

Install Python 3.9 or later, a C compiler, `nm` and GSL.

### Debian or Ubuntu

```bash
sudo apt install build-essential libgsl-dev python3
```

### macOS

```bash
brew install gsl
```

On macOS, install the Xcode command-line tools for the C compiler.

(installation-first-run)=
## Choose a spectral line

List the available lines and use the identifier you want with `--line`.

```bash
python3 peacock.py lines
```

The example below builds the CPU version and runs C II 1334. To use a GPU, follow the [CUDA setup](gpu.md) and select the line in the same way.

```bash
python3 peacock.py build --backend cpu
python3 peacock.py run --line CII1334 --backend cpu --output run/cii
```

The output contains the escaped photon packets. Bin their frequencies to make a line profile. Use a new output directory for each simulation.

(installation-settings)=
## Use your configuration

Pass `--config` for a configuration that matches the line’s reference units and atomic network. Use `--nphot` to set the primary packet count. Cloud sections use `cloud_mode_schema = 2`.

```bash
python3 peacock.py run --line CII1334 --backend cpu --config my-cii.cfg --nphot 4096 --output run/my-cii
```

Build with `--openmp` for CPU threading or `--hdf5` for HDF5 I/O. See the [CUDA guide](gpu.md) for device requirements.
