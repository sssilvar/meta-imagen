#!/bin/bash

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ls ${DATA_FOLDER}

# Run script
echo -e "\n\n[  OK  ] Starting ADMM analysis"
CMD="python3 "${CURRENT_DIR}"/admm.py \
    -f '${DATA_FOLDER}'/groupfile_features_centered.csv \
    -c '${DATA_FOLDER}'/common_data.csv "
eval ${CMD}

# Give permissions
eval "chmod -R 777 "${DATA_FOLDER}
