#!/bin/bash

# Submission script for the Cortical features extraction
#
#OAR -l /nodes=1/core=2,walltime=240:00:00
#OAR -p cputype='xeon'
#
# The job is submitted to the default queue
#OAR -q default
# 

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


python3 ${CURRENT_DIR}/../../imaging/cortical_analysis/scripts/pipeline.py \
-sd /home/ssilvari/Documents/data/ADNI_SURF/ADNI/ \
-gf /home/ssilvari/Documents/data/ADNI_SURF/ADNI/groupfile.csv \
-out /home/ssilvari/Documents/cortical/adni_cortical/