(gpu-transport)=
# GPU setup and advanced workflows

For your first C II spectrum, follow the Linux or Windows commands in
[Getting started](getting-started.md#nvidia-gpu). Use this page to look up your
GPU target, configure an existing CUDA Toolkit, or [submit a single-GPU Slurm job](#run-c-ii-on-one-gpu-with-slurm).

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

(single-gpu-slurm)=
## Run C II on one GPU with Slurm

This job runs the [C II tutorial](getting-started.md#nvidia-gpu) on a cluster.
It follows 100,000 photons through 685 clumps in a 150 km/s radial outflow, then plots
the escaping spectrum. The script reads the configuration and clump catalogue from
[PEACOCK 1.0.2](download.md).

### Set up the environment once

On the login node, extract PEACOCK on a filesystem shared with the compute nodes. Open
the directory containing `peacock.py` and save {download}`cii-one-gpu.slurm <assets/examples/cii/cii-one-gpu.slurm>`
there. Use `module avail` to find your site's C/C++ compiler, GSL and Python modules.
In the commands below and in the script, replace `gcc gsl python` with the same
module names and versions. The cluster supplies the NVIDIA driver on its GPU nodes.

```bash
module load gcc gsl python
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install numpy scipy matplotlib
```

With this environment active, run the **Linux** package-install command under
[Add GPU support](installation.md#add-gpu-support-on-linux-or-windows). This installs
the CUDA compiler library and headers before the job enters the queue.

### Request a GPU and submit the job

The script below requests one GPU and four CPU cores on one node. The CPU cores build
PEACOCK and prepare the input. The GPU transports the photons. The first script argument
sets the [GPU target](#choose-your-gpu-target) for the build.

```{literalinclude} assets/examples/cii/cii-one-gpu.slurm
:language: bash
```

For example, on a cluster with a partition named `gpu` and a GPU type named `a100`,
submit this command from the directory containing `peacock.py`:

```bash
sbatch --partition=gpu --gres=gpu:a100:1 cii-one-gpu.slurm compute_80
```

Use your cluster's partition and GPU type. For an H100, for example, select the site's
H100 resource and pass `compute_90`. If your site requires a billing account, add
`--account=YOUR_ACCOUNT` before the script name.

### Find the log and spectrum

`sbatch` prints a job ID. If it prints `Submitted batch job 12345`, use these commands
from the same source directory, replacing `12345` with your ID:

```bash
squeue -j 12345                       # Check whether the job is waiting or running
tail -f slurm-12345.out               # Follow the log once the job starts (Ctrl-C to exit)
ls run/cii-12345/spectrum.*           # List the results after the job finishes
```

Open **`run/cii-12345/spectrum.png`** to view the line profile. The same directory
contains `spectrum.csv` with the binned flux and its sampling uncertainty, and
`spectrum.json` with the plotting settings. Compare your profile with the
[tutorial spectrum](examples.md#start-with-a-c-ii-simulation).

To reuse the first job's build on the same GPU type with the same software environment,
pass its build directory as a second argument. The next job writes a fresh run directory:

```bash
sbatch --partition=gpu --gres=gpu:a100:1 cii-one-gpu.slurm compute_80 build/cuda-compute_80-12345
```

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
