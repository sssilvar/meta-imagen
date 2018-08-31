#!/bin/bash

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Declare an array containing all the IDs
declare -a IDS=(
   "5b3383924bab0b42506ff78a"  # Center 1
   "5b3383924bab0b42506ff78b"  # Center 2
   "5b3383924bab0b42506ff78c"  # Center 3
   )

for id in 0 1 2 #3 4 5 6
do
    CMD="export DATA_FOLDER=/disk/Data/data_simulation/center_"$((${id} + 1))"/output"
    echo ${CMD}
    eval ${CMD}

    CMD="export CLIENT_ID="${IDS[id]}
    echo ${CMD}
    eval ${CMD}

    COMMON_CSV=${DATA_FOLDER}"/common_data.csv"
    FEATURES_CSV=${DATA_FOLDER}"/groupfile_features.csv"

    echo -e "[  INFO  ] Processing center "$((${id} + 1))" \n\tID: "${CLIENT_ID}

    CMD="python3 "${CURRENT_DIR}"/../admm.py -c "${COMMON_CSV}" -f "${FEATURES_CSV}
    # eval ${CMD}
    echo ${CMD}

    echo -e "\n\n"
done