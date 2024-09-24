#!/usr/bin/bash -l
#SBATCH --job-name=IBC_dose
##SBATCH --account=p200611
##SBATCH --partition=cpu
#SBATCH --nodes=2
#SBATCH --ntasks=4
#SBATCH --cpus-per-task=2
##SBATCH --qos default
##SBATCH --time=01:00:00
#SBATCH --output slurm-%j.out
#SBATCH --error slurm-%j.err
#SBATCH --mail-user erik.knudsen@copenhagenatomics.com
#SBATCH --mail-type END,FAIL
####,FAIL

## Command(s) to run (example):
#module load foss/2023a
#module load SciPy-bundle
#module load tbb
#module load HDF5
#/1.14.0-gompi-2023a
#module load h5py

module use $HOME/modulefiles
module load openmc_chain openmc_xsect/endfb.7.1
module load openmc/0.14.0

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
cases=(1 2 3 4 5)
cn=${cases[$SLURM_ARRAY_TASK_ID]}
cdir=case${cn}
mkdir -p $cdir
cd $cdir
python ../scripts/build_model.py --core ../h5m_files/GIV_core_detailed.h5m --BR ../h5m_files/GIV_BR_detailed.h5m --CR ../h5m_files/GIV_CR_detailed.h5m --case ${cn}  --particles 10000 --batches 550 --inactive 50
pwd
ls
mpirun -np $SLURM_NTASKS --bind-to numa openmc
