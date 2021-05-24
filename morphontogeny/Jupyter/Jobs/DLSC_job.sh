#!/bin/bash
 
#SBATCH -n 4 							# number of cores
#SBATCH -p publicgpu					# partition name
#SBATCH -q wildfire						# QOS
#SBATCH --mem=32GB						# memory
#SBATCH -t 0-04:00						# wall time (D-HH:MM)
#SBATCH -o slurm.%j.out					# STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err					# STDERR (%j = JobId)
#SBATCH --mail-type=ALL					# Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=mabbasi6@asu.edu	# send-to address

python /home/mabbasi6/Jupyter/Jobs/DLSC.py