#!/bin/bash
#script to clip and concatenate CMIP6 files 

#SBATCH --job-name = pre_process_CMIP6                              # name your job
#SBATCH -n 1                                                              # specify number of tasks
#SBATCH -p workq
#SBATCH -N 1                                              # number of nodes
#SBATCH --account=nhvtwsc                    # your account code, seen when you first log in
#SBATCH --time=2-00:00:00                                                     # time D-HH:MM:SS
#SBATCH --mail-type=ALL                                               # choose when you want to be emailed
#SBATCH --mail-user=mholland@usgs.gov                     # add your email address
#SBATCH -o slurm_cdo.out                           # name of output file

module load cdo

srun python cdo_CMIP6_MV.py
