#!/bin/bash


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


ls ${DATA_FOLDER}

# Run script
echo -e "\n\n[  OK  ] Starting statistical analysis"
CMD="python3 "${CURRENT_DIR}"/center_data.py \
    -data "${DATA_FOLDER}"/groupfile_features.csv"
eval ${CMD}

# Give permissions
eval "chmod -R 766 "${DATA_FOLDER}
