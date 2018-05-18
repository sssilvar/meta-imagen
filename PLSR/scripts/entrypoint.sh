#!/bin/bash


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "\n\n[  OK  ] Starting statistical analysis"

CMD="python3 "${CURRENT_DIR}"/py/plsr_analysis.py \
    -x /user/ssilvari/home/Documents/temp/output/groupfile_thick.csv \
    -y /user/ssilvari/home/Documents/temp/output/groupfile_thick.csv " #${DATA_FOLDER}"/log.log"
eval ${CMD}
eval "chmod -R 766 "${DATA_FOLDER}
