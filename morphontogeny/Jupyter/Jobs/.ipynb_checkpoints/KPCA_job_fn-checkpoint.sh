#!/bin/bash

#SBATCH -p fn					# partition name

#SBATCH -N 1                        # number of compute nodes
#SBATCH -n 2 							# number of cores, 27,617 MB memory for each core
#SBATCH -t 2-00:00						# wall time (D-HH:MM)
#SBATCH -o slurm.%j.out					# STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err					# STDERR (%j = JobId)
#SBATCH --mail-type=ALL					# Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=mabbasi6@asu.edu	# send-to address

python /home/mabbasi6/Jupyter/Jobs/KPCA_sigmoid.py