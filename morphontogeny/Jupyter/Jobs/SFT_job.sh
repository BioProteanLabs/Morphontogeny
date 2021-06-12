#!/bin/bash

#SBATCH -n 6 							# number of cores
#SBATCH -p publicgpu					# partition name
#SBATCH -q wildfire						# QOS
#SBATCH -t 0-12:00						# wall time (D-HH:MM)
#SBATCH -o slurm.%j.out					# STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err					# STDERR (%j = JobId)
#SBATCH --mail-type=ALL					# Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=mabbasi6@asu.edu	# send-to address

python ~/git/Morphontogeny/morphontogeny/Jupyter/Jobs/SFT.py