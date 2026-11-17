#!/bin/bash -l
#SBATCH --job-name=peacock-cii
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out

set -e
cd "${SLURM_SUBMIT_DIR:?Submit from the extracted PEACOCK directory}"

# Use the same module names and versions used to create .venv.
module load gcc gsl python
source .venv/bin/activate

arch=${1:?Supply the target for the requested GPU, e.g. compute_80 for an A100}
run_dir="run/cii-${SLURM_JOB_ID}"
build_dir=${2:-"build/cuda-${arch}-${SLURM_JOB_ID}"}
if [[ $# -lt 2 ]]; then
    python3 peacock.py build --backend cuda --arch "$arch" \
        --jobs "$SLURM_CPUS_PER_TASK" --output "$build_dir"
fi

python3 peacock.py run --backend cuda --line CII1334 --build-dir "$build_dir" \
    --config examples/cii/quickstart.cfg \
    --clump-file examples/cii/quickstart-clumps.txt --output "$run_dir"
python3 tools/plot_spectrum.py "$run_dir" --output "$run_dir/spectrum.png"
printf 'Spectrum: %s/%s/spectrum.png\n' "$PWD" "$run_dir"
