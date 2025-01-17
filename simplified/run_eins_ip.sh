#!/usr/bin/bash -l
#SBATCH --job-name "g4_ip"
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=2
##SBATCH --time=24:30:00
#SBATCH --output slurm-%j.out
#SBATCH --error slurm-%j.err
#SBATCH --mail-user erik.knudsen@copenhagenatomics.com
#SBATCH --mail-type BEGIN,END,FAIL
####,FAIL

module use $HOME/modulefiles
module load openmc_chain openmc_xsect/endfb.7.1
module load openmc/0.14.0

model=in_parts
cases=(5)
cs=${cases[$SLURM_ARRAY_TASK_ID]}
for cs in $cases; do
  mkdir -p ${model}_case${cs}
  cd ${model}_case${cs}
  echo running model $model case $cs
  ln -sf ../h5m_files .
  python ../scripts/build_model.py --type $model -p 10000 -b 550 -i 50 --case ${cs}
  ls
  echo $PWD
  sleep 2
  mpirun --bind-to numa -np $SLURM_NTASKS openmc
  cd ..
done
