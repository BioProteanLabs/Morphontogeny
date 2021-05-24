#!/bin/bash

#SBATCH -n 10 							# number of cores
#SBATCH --mem=56GB						# memory
#SBATCH -p asing250cpu1					# partition name
#SBATCH -q wildfire						# QOS
#SBATCH -t 7-00:00						# wall time (D-HH:MM)
#SBATCH -o slurm.%j.out					# STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err					# STDERR (%j = JobId)
#SBATCH --mail-type=ALL					# Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=mabbasi6@asu.edu	# send-to address

python /home/mabbasi6/Jupyter/Jobs/KPCA_poly.py