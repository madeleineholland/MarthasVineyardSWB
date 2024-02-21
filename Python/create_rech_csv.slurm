#!/bin/bash

#SBATCH --job-name=Marthas_Vineyard_SWB_csv			  # name your job
#SBATCH --ntasks=1							          # specify number of tasks
#SBATCH --nodes=1                      		  # number of nodes
#SBATCH --account=nhvtwsc                    # your account code, seen when you first log in
#SBATCH --time=3-00:00:00						      # time D-HH:MM:SS 
#SBATCH --mail-type=ALL						      # choose when you want to be emailed
#SBATCH --mail-user=mholland@usgs.gov			  # add your email address
#SBATCH -o summary.out                           # name of output file


python3 create_recharge_csv_v2.py
