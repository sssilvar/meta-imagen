# This script runs the ENIGMA Shape pipeline and
# the extraction of cortical thickness and jacobians.
# 
# This will be taken as input of the statistical analysis

# ==== FOLDERS ====
FS_FOLDER=${1-"/user/ssilvari/home/Documents/temp/input"}
OUTPUT_FOLDER=${2-"/user/ssilvari/home/Documents/temp/output"}
GROUPFILE_FOLDER=${3-"/user/ssilvari/home/Documents/temp/group"}

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ENIGMA Shape pipeline
echo -e "\n\n======= ENIGMA SHAPE ======="
SCRIPT=${CURRENT_DIR}"/../imaging/eshape/build.sh"
CMD="bash "${SCRIPT}" "${FS_FOLDER}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
echo ${CMD}

# Cortical feature extraction
echo -e "\n\n======= CORTICAL ======="
SCRIPT=${CURRENT_DIR}"/../imaging/cortical_analysis/build.sh"
CMD="bash "${SCRIPT}" "${FS_FOLDER}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
echo ${CMD}

