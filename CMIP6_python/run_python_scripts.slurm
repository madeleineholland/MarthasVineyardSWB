#!/bin/bash

#SBATCH --job-name=preprocess_climate_input				  # name your job
#SBATCH --ntasks=4 							          # specify number of tasks
#SBATCH --nodes=2                       		  # number of nodes
#SBATCH --account=nhvtwsc                    # your account code, seen when you first log in
#SBATCH --time=2-00:00:00						      # time D-HH:MM:SS 
#SBATCH --mail-type=ALL						      # choose when you want to be emailed
#SBATCH --mail-user=mholland@usgs.gov			  # add your email address
#SBATCH -o snakemake.out                           # name of output file


module load cdo

python cdo_CMIP6_MV.py
python daily2monthly.py
