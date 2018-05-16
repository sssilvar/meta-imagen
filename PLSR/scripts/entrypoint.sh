#!/bin/bash


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "\n\n[  OK  ] Starting statistical analysis"

CMD="python3 "${CURRENT_DIR}"/test_plsr.py > "${DATA_FOLDER}"/log.log"
eval ${CMD}
eval "chmod -R 766 "${DATA_FOLDER}
