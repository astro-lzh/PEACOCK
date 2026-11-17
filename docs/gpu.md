# GPU transport

One CUDA build runs all 14 packaged line profiles. Select a line with `--line` at run
time. The [C II walkthrough](getting-started.md) uses the same physical configuration on
CPU and GPU.

(gpu-requirements)=
## Install the GPU requirements

Follow [Installation](installation.md#add-gpu-support-on-linux-or-windows) to install
the host tools, Python environment, NVIDIA driver, and CUDA components. Use Linux or
Windows with a CUDA-capable NVIDIA GPU.

## Choose your GPU target

The target tells the compiler which GPU instructions to generate. First find the GPU model:

```text
nvidia-smi --query-gpu=name,driver_version --format=csv
```

Find that exact model in [NVIDIA's compute-capability table](https://developer.nvidia.com/cuda-gpus).
For example, capability 8.6 corresponds to the PEACOCK argument `--arch compute_86`.

| GPU example | Compute capability | Build argument |
| --- | --- | --- |
| GeForce RTX 3090 | 8.6 | `--arch compute_86` |
| GeForce RTX 4090 | 8.9 | `--arch compute_89` |
| GeForce RTX 5090 | 12.0 | `--arch compute_120` |
| NVIDIA A100 | 8.0 | `--arch compute_80` |
| NVIDIA H100 | 9.0 | `--arch compute_90` |

The installed CUDA compiler must also support the target. In particular, `compute_120`
requires CUDA 12.8 or later. Explicitly pass your target when building; the command-line
default is `compute_120`.

(gpu-run)=
## Build once and run the C II example

The commands below use an RTX 5090 target. Replace `compute_120` with the target selected
above. Run them from the source directory with the Python environment active.

### Linux

```bash
python3 peacock.py build --backend cuda --arch compute_120 --output build/cuda
python3 peacock.py run --line CII1334 --backend cuda --build-dir build/cuda --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --nphot 4096 --output run/cii-cuda
python3 tools/plot_spectrum.py run/cii-cuda --output run/cii-cuda/spectrum.png
```

### Windows PowerShell

Use the Windows Python environment and UCRT64 tools from the
[Windows installation instructions](installation.md#windows):

```powershell
.\.venv\Scripts\python.exe peacock.py build --backend cuda --arch compute_120 --compiler-prefix C:/msys64/ucrt64 --output build/cuda
.\.venv\Scripts\python.exe peacock.py run --line CII1334 --backend cuda --build-dir build/cuda --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --nphot 4096 --output run/cii-cuda
.\.venv\Scripts\python.exe tools/plot_spectrum.py run/cii-cuda --output run/cii-cuda/spectrum.png
```

Use a new build directory the first time, and a new or empty output directory for each
simulation. Reuse the build when changing the spectral line, model parameters, or photon
count. Choose a new build directory when changing the compiler, CUDA target, or PEACOCK
source version, then pass the new directory with `--build-dir`.

The plotter selects escaped packets and uses the same velocity and continuum normalization
for CPU and CUDA output. See [Reading the outputs](outputs.md). Monte Carlo packet histories
can differ between the two implementations; a small-photon example is useful for learning
the workflow, while scientific comparisons need enough photons to assess sampling noise.

## Run a different line

The same build runs these examples without recompilation:

```bash
python3 peacock.py run --line CIV1548 --backend cuda --build-dir build/cuda --output run/civ
python3 peacock.py run --line SiII1190 --backend cuda --build-dir build/cuda --output run/si1190-cuda
```

On Windows, replace `python3` with `.\.venv\Scripts\python.exe`.

## Use an existing CUDA Toolkit

PEACOCK can also use a complete system Toolkit. Supply its compiler library and header
directory explicitly. For a Linux Toolkit installed at `/usr/local/cuda`:

```bash
python3 peacock.py build --backend cuda --arch compute_120 --nvrtc-library /usr/local/cuda/lib64/libnvrtc.so --cuda-include /usr/local/cuda/include --cuda-include /usr/local/cuda/include/cccl --output build/cuda-toolkit
```

For a Windows CUDA 12.8 Toolkit installed in NVIDIA's usual directory:

```powershell
.\.venv\Scripts\python.exe peacock.py build --backend cuda --arch compute_120 --compiler-prefix C:/msys64/ucrt64 --nvrtc-library "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/bin/nvrtc64_120_0.dll" --cuda-include "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/include" --cuda-include "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/include/cccl" --output build/cuda-toolkit
```

Use your installed Toolkit's paths and target. Additional `--cuda-include` arguments can
be supplied when CUDA, cuRAND, and CCCL headers are in separate directories. The
[Python-package installation](installation.md#add-gpu-support-on-linux-or-windows) normally
finds these locations automatically.

(gpu-staged)=
## Prepare and execute separately

For a batch of simulations or a compute cluster, input preparation and GPU execution can
be separate steps. Both use the same build and selected line:

```bash
python3 peacock.py prepare --line CII1334 --build-dir build/cuda --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/cii-staged
python3 peacock.py execute --line CII1334 --build-dir build/cuda --input run/cii-staged
```

For a custom cloud catalogue, pass `--config` and `--clump-file` during preparation. Keep
the resulting case directory together when transferring it to another machine. Build the
native program for the operating system on which preparation runs, and compile the CUDA
module for the GPU on which execution runs.

(gpu-host-only)=
## Prepare inputs without a GPU build

If a machine will only prepare inputs, build the host preparation program:

```bash
python3 peacock.py build --backend cuda --host-only --output build/cuda-host
python3 peacock.py prepare --line CII1334 --build-dir build/cuda-host --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --output run/cii-inputs
```

Execution needs a complete CUDA build. When a cluster provides CUDA and GSL through
environment modules, load the appropriate modules before building and in the submitted
job. Module names are specific to the cluster.

## Control GPU memory use

The `--batch` option controls the number of packets processed together; its default is
1024. A smaller value can reduce packet-buffer memory use:

```bash
python3 peacock.py run --line CII1334 --backend cuda --build-dir build/cuda --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt --batch 256 --output run/cii-small-batch
```

The gas grid and cloud catalogue also occupy device memory. More photons improve the
Monte Carlo estimate but take longer to process. Keep the model configuration and observing
choices fixed when checking how a spectrum changes with photon count.
