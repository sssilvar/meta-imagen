#!/usr/bin/env bash

# Run the Cortical Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved

# ==== FOLDERS ====
FS_DATASET="/disk/Data/center_simulation/test/input"
OUTPUT_FOLDER="/disk/Data/center_simulation/test/output"
GROUPFILE_FOLDER="/disk/Data/center_simulation/test/group"

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT=${CURRENT_DIR}"/../imaging/cortical_analysis/build.sh"

CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
eval ${CMD}
