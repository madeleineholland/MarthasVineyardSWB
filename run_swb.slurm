#!/bin/bash

#SBATCH --job-name=Marthas_Vineyard_SWB_test				  # name your job
#SBATCH --ntasks=1							          # specify number of tasks
#SBATCH --nodes=1                      		  # number of nodes
#SBATCH --account=nhvtwsc                    # your account code, seen when you first log in
#SBATCH --time=1-00:00:00						      # time D-HH:MM:SS 
#SBATCH --mail-type=ALL						      # choose when you want to be emailed
#SBATCH --mail-user=mholland@usgs.gov			  # add your email address
#SBATCH -o snakemake_run1.out                           # name of output file


module switch PrgEnv-cray PrgEnv-gnu
module load swb2 

srun snakemake -s Snakefile_MV_CMIP6.smk -j10
