#!/bin/bash

# Get client params
CENTER_FOLDER=$1
ID=$2
SERVER=${3-'http://localhost:3300/'}

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set main folders
FS_DATASET=${CENTER_FOLDER}"/input"
OUTPUT_FOLDER=${CENTER_FOLDER}"/output"
GROUPFILE_FOLDER=${CENTER_FOLDER}"/group"

# 1. Center data (Welford)
SCRIPT=${CURRENT_DIR}"/../centering_data/build.sh"
CMD="bash "${SCRIPT}" "${OUTPUT_FOLDER}" "${ID}" "${SERVER}
echo ${CMD}
eval ${CMD}

# 2. Distributed ADMM
SCRIPT=${CURRENT_DIR}"/../ADMM/build.sh"
CMD="bash "${SCRIPT}" "${OUTPUT_FOLDER}" "${ID}" "${SERVER}
echo ${CMD}
eval ${CMD}

# 3. PLSR
SCRIPT=${CURRENT_DIR}"/../PLSR/build.sh"
CMD="bash "${SCRIPT}" "${OUTPUT_FOLDER}" "${ID}" "${SERVER}
echo ${CMD}
eval ${CMD}

