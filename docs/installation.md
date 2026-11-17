# Installation

Install the tools below once, then follow [your first C II simulation](getting-started.md).
The same model configuration is used whether photons are transported on a CPU or an
NVIDIA GPU.

Start by extracting the [source ZIP](download.md). Run the commands from the extracted
`PEACOCK` directory, which contains `peacock.py`.

## What to install

| Component | Used for |
| --- | --- |
| Python 3.9 or later | Running PEACOCK commands. Python 3.12 or 3.13 is a convenient choice for a new installation. |
| A C compiler, `nm`, and GSL | Building the transport program. GPU preparation also needs a C++ compiler. |
| NumPy, SciPy, and Matplotlib | Preparing GPU inputs, reading packet files, and making the tutorial spectrum. |
| NVIDIA driver and CUDA components | GPU transport on Linux or Windows. These are additional to the CPU tools. |

The sections below install the dependencies for the complete tutorial. OpenMP and HDF5
are [optional](#optional-cpu-features).

(install-linux)=
## Linux: Debian or Ubuntu

These commands use the system Python on Ubuntu 22.04 or later, or Debian 12 or later.

```bash
sudo apt update
sudo apt install build-essential binutils libgsl-dev python3 python3-venv
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numpy scipy matplotlib
```

Keep this environment active when building, running, and plotting. In a new terminal,
return to the source directory and run `. .venv/bin/activate` again.

(install-macos)=
## macOS

Install [Homebrew](https://brew.sh/) if it is not already available. The Xcode command-line
tools provide the compiler; Homebrew provides Python and GSL.

```bash
xcode-select --install
brew install python@3.12 gsl
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install numpy scipy matplotlib
```

If Xcode reports that its command-line tools are already installed, continue with the
Homebrew command. PEACOCK finds GSL through the `gsl-config` program installed by Homebrew.

Use CPU transport on macOS. The CUDA instructions below require a supported NVIDIA GPU
on Linux or Windows.

(install-windows)=
## Windows

Use x86-64 Windows and x86-64 Python. Install [MSYS2](https://www.msys2.org/) in its usual
location, `C:\msys64`, and install [Python](https://www.python.org/downloads/windows/).
Python 3.12 or 3.13 works well with the tutorial packages.

### 1. Install the compiler and GSL in MSYS2 UCRT64

Open **MSYS2 UCRT64** from the Start menu. Update its packages:

```bash
pacman -Syu
```

If the update asks you to close the terminal, close it, reopen **MSYS2 UCRT64**, and finish
the update before installing the tools:

```bash
pacman -Su
pacman -S --needed mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-binutils mingw-w64-ucrt-x86_64-gsl
```

These are the [UCRT64 compiler and libraries](https://www.msys2.org/docs/environments/).
Keep them in the same environment.

### 2. Create a Python environment in PowerShell

Open **PowerShell** in the extracted `PEACOCK` directory. Use the regular Windows Python
installation for the following commands:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install numpy scipy matplotlib
```

The explicit Python path avoids the need to change PowerShell's activation policy. In
later examples, replace `python3` with `.\.venv\Scripts\python.exe`. When building on
Windows, also pass `--compiler-prefix C:/msys64/ucrt64`, or the location where you installed
UCRT64.

Continue with the Windows commands in the [first simulation](getting-started.md) or
[GPU guide](gpu.md) to build PEACOCK.

(install-cuda)=
## Add GPU support on Linux or Windows

First install the tools for your operating system above. Then install an NVIDIA driver
that supports your GPU. Check that the driver sees the card:

```text
nvidia-smi
```

The CUDA (or CUDA UMD) version shown by `nvidia-smi` describes the driver's supported CUDA version;
it does not establish that the CUDA compiler libraries or headers are installed. NVIDIA's
[driver documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html) explains this
field.

The following route installs matching CUDA 12.8 components directly from NVIDIA
[Python packages](https://pypi.org/project/cuda-toolkit/12.8.2/) into the environment used by
PEACOCK. The four packages supply the compiler library, runtime headers, random-number
headers, and C++ headers. They do not install the GPU driver.

On Linux, with `.venv` active:

```bash
python3 -m pip install nvidia-cuda-nvrtc-cu12==12.8.93 nvidia-cuda-runtime-cu12==12.8.90 nvidia-curand-cu12==10.3.9.90 nvidia-cuda-cccl-cu12==12.8.90
```

On Windows, in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install nvidia-cuda-nvrtc-cu12==12.8.93 nvidia-cuda-runtime-cu12==12.8.90 nvidia-curand-cu12==10.3.9.90 nvidia-cuda-cccl-cu12==12.8.90
```

PEACOCK normally finds these packages automatically. CUDA 12.8 introduced compiler support
for Blackwell targets, including the RTX 5090's `compute_120` target; an older compiler
cannot build that target. See the [CUDA 12.8 features](https://docs.nvidia.com/cuda/archive/12.8.2/cuda-features-archive/index.html).
The driver must support your particular card and the selected CUDA components.

Next, [choose your GPU target and build PEACOCK](gpu.md#choose-your-gpu-target). If you
already use a complete system CUDA Toolkit, the GPU guide also explains how to point
PEACOCK to that installation.

(optional-cpu-features)=
## Optional CPU features

The first simulation works without these options. Use a new build directory when enabling
one of them, then pass that directory with `--build-dir` when running.

### CPU threads with OpenMP

On Linux, the GCC compiler installed above supplies OpenMP support:

```bash
python3 peacock.py build --backend cpu --openmp --output build/cpu-openmp
export OMP_NUM_THREADS=4
python3 peacock.py run --line CII1334 --backend cpu --build-dir build/cpu-openmp --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/cii-openmp
```

On macOS, install the [OpenMP runtime](https://formulae.brew.sh/formula/libomp) and tell
Apple Clang where to find it:

```bash
brew install libomp
export OPENMP_CFLAGS="-Xpreprocessor -fopenmp -I$(brew --prefix libomp)/include"
export OPENMP_LIBS="-L$(brew --prefix libomp)/lib -lomp"
python3 peacock.py build --backend cpu --openmp --output build/cpu-openmp
export OMP_NUM_THREADS=4
```

In Windows PowerShell, use UCRT64's GCC and set the number of threads for the current shell:

```powershell
.\.venv\Scripts\python.exe peacock.py build --backend cpu --openmp --compiler-prefix C:/msys64/ucrt64 --output build/cpu-openmp
$env:OMP_NUM_THREADS = "4"
```

The build option `--jobs` controls parallel compilation. `OMP_NUM_THREADS` controls CPU
transport at run time; the two settings serve different purposes.

### HDF5 files

HDF5 I/O requires HDF5 development files and `pkg-config`. On Debian or Ubuntu:

```bash
sudo apt install libhdf5-dev pkg-config
pkg-config --modversion hdf5
python3 peacock.py build --backend cpu --hdf5 --output build/cpu-hdf5
```

On macOS, install them with `brew install hdf5 pkgconf`. On Windows, install
`mingw-w64-ucrt-x86_64-hdf5` and `mingw-w64-ucrt-x86_64-pkgconf` in MSYS2 UCRT64, and
include `--compiler-prefix C:/msys64/ucrt64` in the build command.

The tutorial uses ordinary ASCII packet output. The default CPU build is sufficient for
the [first run](getting-started.md).

## Continue to the first simulation

Follow the [C II walkthrough](getting-started.md) to build, run, and plot the same physical
model. If installation stops with an error, see [Common questions](troubleshooting.md).
