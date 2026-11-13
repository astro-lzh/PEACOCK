# GPU transport

Run all 14 PEACOCK line profiles with one CUDA build.

(gpu-requirements)=

## What you need for a GPU run

### Check your GPU and driver

Use a CUDA-capable NVIDIA GPU with a compatible NVIDIA driver.

### Set up Python

Install Python 3.9 or later, plus NumPy and SciPy. PEACOCK uses them to prepare simulation inputs and read the results.

### Install the tools that build PEACOCK

PEACOCK needs C and C++ compilers, the `nm` tool and the GNU Scientific Library (GSL). On Windows, MSYS2 UCRT64 can provide all three.

### Install NVIDIA’s CUDA build files

PEACOCK uses NVIDIA’s CUDA compiler library and headers. You can get them from the CUDA Toolkit or compatible NVIDIA Python packages.

The build command below targets `compute_120`, which works with an RTX 5090. If your GPU needs a different target, add `--arch` followed by the target for that GPU. The `docs/gpu-workflow.md` file in the source archive explains how to point PEACOCK to your CUDA installation.

(gpu-run)=

## Build once and run a line

Use a new or empty directory for each run.

```bash
python3 peacock.py build --backend cuda
python3 peacock.py run --line CIV1548 --backend cuda --output run/civ
python3 peacock.py run --line SiII1190 --backend cuda --output run/si1190-cuda
```

(gpu-staged)=

## Prepare and execute separately

Use the same build for different lines. Use the matching line ID for a case's preparation and execution. For a custom catalogue, pass --config and --clump-file during preparation.

```bash
python3 peacock.py prepare --line SiII1190 --output run/si1190-staged
python3 peacock.py execute --line SiII1190 --input run/si1190-staged
```

(gpu-host-only)=

## Prepare on the host

A host-only build creates the input exporter. The prepare command writes the grid and initial packets for later CUDA execution.

```bash
python3 peacock.py build --backend cuda --host-only --output build/cuda-host
python3 peacock.py prepare --line SiII1190 --build-dir build/cuda-host --output run/si1190-inputs
```
