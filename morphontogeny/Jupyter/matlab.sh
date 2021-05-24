#!/bin/bash

#SBATCH --job-name=simple_matlab    # job name
#SBATCH -n 1                        # number of cores
##SBATCH -p parallel                # parallel processing
#SBATCH -t 0-00:01                  # run time (D-HH:MM)
#SBATCH -o slurm.%j.out             # STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err             # STDERR (%j = JobId)
##SBATCH --mail-type=ALL            # Send a notification
##SBATCH --mail-user=mabbasi6@asu.edu # send-to address

module load matlab/2020a

matlab –nodisplay –nodesktop –nosplash < hello.m
##matlab –nodisplay –nodesktop –nosplash –r “hello, quit"
