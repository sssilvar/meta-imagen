#!/bin/bash

# Run the ENIGMA Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved

# ==== FOLDERS ====
FS_DATASET="/user/ssilvari/home/Documents/temp/input"
OUTPUT_FOLDER="/user/ssilvari/home/Documents/temp/output"
GROUPFILE_FOLDER="/user/ssilvari/home/Documents/temp/group"

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT=${CURRENT_DIR}"/../imaging/eshape/build.sh"

CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
eval ${CMD}
