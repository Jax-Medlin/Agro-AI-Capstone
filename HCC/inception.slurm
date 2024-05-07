#!/bin/bash
#SBATCH --nodes=2
#SBATCH --mem=100gb
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --time=72:00:00
#SBATCH --job-name=inceptionv3_05022023
#SBATCH --error=inceptionv3_05022023.%J.err
#SBATCH --output=inceptionv3_05022023.%J.out

#module load python/3.9
source .venv/bin/activate
python /work/hsiycsci4970/jaxmedlin/handheld_ouput/inceptionv3_model.py
