#!/usr/bin/env bash

# Parse arguments
OUTPUT_FOLDER=$1
ID=$2

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Execute ADMM
CMD="bash "${CURRENT_DIR}"/../ADMM/build.sh "${OUTPUT_FOLDER}" "${ID}
eval ${CMD}
