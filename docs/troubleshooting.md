(common-questions)=
# Troubleshooting

Look for the error message or symptom below. If the problem began after editing
a model, try the supplied [C II example](getting-started.md) to check whether the
installation works with its original inputs.

## The build cannot find GSL or `nm`

PEACOCK needs the GNU Scientific Library (GSL) and the compiler tools listed
in the [platform instructions](installation.md). On Linux or macOS,
these commands show whether your terminal can find them.

```bash
command -v cc
command -v nm
gsl-config --version
```

On Windows, use the UCRT64 packages and include `--compiler-prefix C:/msys64/ucrt64` in the
build command. This gives PEACOCK the compiler, header, library, and runtime locations from
the same installation. A missing `gsl/gsl_*.h` header requires the development files;
installing only a runtime library is insufficient.

## The build directory already exists

PEACOCK creates a new build directory and records the compiler and source used. Reuse the
existing build for later runs, or choose another directory for a different build:

```bash
python3 peacock.py build --backend cpu --openmp --output build/cpu-openmp
python3 peacock.py run --line CII1334 --backend cpu --build-dir build/cpu-openmp --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/cii-openmp
```

Use the same `--build-dir` in every command that should use that build. Changing `--line`
or model parameters does not require compilation. After upgrading PEACOCK, build the new
source in a new directory.

## The output directory is not empty

Choose another output name, such as `run/cii-second`. Keep the previous run if it contains
results you need. A separate directory for each simulation also keeps its configuration
and packet files together.

## NVRTC or a CUDA header cannot be found

NVRTC is the NVIDIA compiler library that PEACOCK uses to build its GPU program.
Run the [GPU installation command](installation.md#add-gpu-support-on-linux-or-windows)
in the same Python environment you use to build PEACOCK. It installs the compiler
library and the header files it needs.

For a complete system Toolkit, use the explicit `--nvrtc-library` and `--cuda-include`
arguments shown in [GPU setup](gpu.md#use-an-existing-cuda-toolkit). If packages were
installed into a different Python environment, activate the correct one or pass
`--nvidia-root` pointing to the directory containing `cuda_nvrtc`, `cuda_runtime`, `curand`,
and `cuda_cccl`.

## The compiler does not recognize my GPU target

Check both the card's [compute capability](gpu.md#choose-your-gpu-target) and the compiler
version. For example, `compute_120` requires CUDA 12.8 or later. Choose your card's target
explicitly with `--arch` and build into a new directory.

If compilation succeeds but execution reports an unsupported PTX version, update the
NVIDIA driver to a version compatible with the CUDA compiler used. The version shown by
`nvidia-smi` describes driver support, while the Python CUDA packages or system Toolkit
supply the compiler.

(windows-blocks-a-compiler-with-application-control-error-4551)=
## Windows reports Application Control error 4551

Check which file Windows blocked and when the message appeared.

- **During the build, `g++.exe`.** Windows has blocked the C++ compiler.
  The [Windows GPU tutorial](getting-started.md#nvidia-gpu) shows how to select
  Clang with `--cxx`. On a managed computer, use a compiler approved by your
  administrator.
- **At the start of the run, `peacock-export.exe`.** This program prepares the
  cloud grid and initial photons. Give your administrator the executable path and
  its `executable_sha256` value from `build.json` so they can identify the exact
  file. The [Microsoft troubleshooting guide](https://learn.microsoft.com/windows/security/application-security/application-control/app-control-for-business/operations/appcontrol-debugging-and-troubleshooting)
  explains where to find the blocked file in the CodeIntegrity event log.

Windows 11 Smart App Control has no per-app exception. If it blocks a locally built
exporter, Microsoft recommends a build signed with a trusted code-signing certificate.
See the [Microsoft Smart App Control FAQ](https://support.microsoft.com/en-us/windows/security/threat-malware-protection/smart-app-control-frequently-asked-questions).

## Windows reports a missing DLL

Keep the UCRT64 installation used for the build available at its recorded location. Build
with `--compiler-prefix` so PEACOCK can supply its runtime directory when launching the
program. Keep the complete build directory and source distribution together; copying only
the executable omits files needed for a normal PEACOCK run.

For an NVRTC DLL error, check that the compiler library and its `nvrtc-builtins` DLL come
from the same CUDA installation. The [NVIDIA Python packages](installation.md#add-gpu-support-on-linux-or-windows)
provide a matching set.

## OpenMP or HDF5 fails to compile

First try the ordinary CPU build. Add the optional feature after installing its
[extra dependencies](installation.md#optional-cpu-features), and use a new build directory.
Apple Clang needs the OpenMP include and library flags shown in the installation guide.
For HDF5, `pkg-config --modversion hdf5` should succeed before enabling `--hdf5`.

## The requested line is not available

List the line names this installation accepts.

```bash
python3 peacock.py lines
```

Use the name for the reference transition you want. For a multiplet, PEACOCK also
follows the coupled transitions listed in the [line table](choosing-a-line-and-an-observable.md).
Every listed line can run on an NVIDIA GPU. In this release, C IV and Mg II
require a GPU.

Research figures may show applications beyond the selectors in the downloaded release.
For example, the Si III and Si IV figures in [Examples](examples.md) do not supply a new
command-line selector.

## The plotted spectrum is noisy or empty

**Noisy profile.** A velocity bin with few photons has a large sampling uncertainty.
Increase `--nphot` and keep the same wind and plotting settings to obtain a smoother
profile.

**Empty profile.** Start with the terminal message and run summary. If photons
escaped, check how many fell inside your aperture and plotted velocity range. If
none escaped, inspect the model configuration and absorption. The
[output guide](outputs.md) shows where to find each count.

## Get help

Show the available options with:

```bash
python3 peacock.py --version
python3 peacock.py --help
python3 peacock.py build --help
python3 peacock.py run --help
```

If a problem remains, open an [issue in the PEACOCK repository](https://github.com/astro-lzh/PEACOCK/issues).
Include your PEACOCK version, operating system, the full command, the error message, and a
small configuration that reproduces it. For GPU issues, add the GPU model, driver version,
chosen `--arch`, and CUDA package or Toolkit version.
