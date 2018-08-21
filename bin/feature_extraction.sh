# This script runs the ENIGMA Shape pipeline and
# the extraction of cortical thickness and jacobians.
# 
# This will be taken as input of the statistical analysis

# ==== FOLDERS ====
FS_FOLDER=${1-"/disk/Data/dataset"}
OUTPUT_FOLDER=${2-"/disk/Data/center_simulation/all_in_one/output"}
GROUPFILE_FOLDER=${3-"/disk/Data/center_simulation/all_in_one/group"}

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ENIGMA Shape pipeline
echo -e "\n\n======= ENIGMA SHAPE ======="
SCRIPT=${CURRENT_DIR}"/../imaging/eshape/build.sh"
CMD="bash "${SCRIPT}" "${FS_FOLDER}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
eval ${CMD}

# Cortical feature extraction
echo -e "\n\n======= CORTICAL ======="
SCRIPT=${CURRENT_DIR}"/../imaging/cortical_analysis/build.sh"
CMD="bash "${SCRIPT}" "${FS_FOLDER}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
eval ${CMD}

