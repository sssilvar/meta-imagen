#!/bin/bash


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


ls ${DATA_FOLDER}

# Run script
# TODO: return to _admm.csv
echo -e "\n\n[  OK  ] Starting statistical analysis"
CMD="python3 "${CURRENT_DIR}"/plsr_analysis.py \
    -x '${DATA_FOLDER}'/groupfile_features.csv \
    -y '${DATA_FOLDER}'/groupfile_features.csv " #${DATA_FOLDER}"/log.log"
eval ${CMD}

# Give permissions
eval "chmod -R 777 "${DATA_FOLDER}
