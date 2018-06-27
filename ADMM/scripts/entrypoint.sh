#!/bin/bash


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


ls ${DATA_FOLDER}

# Run script
echo -e "\n\n[  OK  ] Starting ADMM analysis"
CMD="python3 "${CURRENT_DIR}"/plsr_analysis.py \
    -x '${DATA_FOLDER}'/groupfile_thick.csv \
    -y '${DATA_FOLDER}'/groupfile_thick.csv " #${DATA_FOLDER}"/log.log"
eval ${CMD}

# Give permissions
# eval "chmod -R 766 "${DATA_FOLDER}
