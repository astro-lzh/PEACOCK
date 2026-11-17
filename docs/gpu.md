(gpu-transport)=
# GPU setup and advanced workflows

For your first C II spectrum, follow the Linux or Windows commands in
[Getting started](getting-started.md#nvidia-gpu). Use this page to look up your
GPU target, configure an existing CUDA Toolkit, or run on a cluster.

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
(build-once-and-run-the-c-ii-example)=
## Run a different line

After the [first GPU run](getting-started.md#nvidia-gpu), the compiled CUDA module runs
all 14 packaged line profiles. Use `--line` to select the atomic data. For example,

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
$ucrt = "C:/msys64/ucrt64"
.\.venv\Scripts\python.exe peacock.py build --backend cuda --arch compute_120 --compiler-prefix "$ucrt" --cxx "$ucrt/bin/clang++.exe" --nvrtc-library "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/bin/nvrtc64_120_0.dll" --cuda-include "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/include" --cuda-include "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.8/include/cccl" --output build/cuda-toolkit
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
