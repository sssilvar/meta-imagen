#!/usr/bin/env bash

# Run the ENIGMA Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved

# ==== FOLDERS ====
#MAIN_FOLDER="/user/ssilvari/home/Documents/Data/center_simulation/all_in_one/"
MAIN_FOLDER="/user/ssilvari/home/Documents/Data/center_simulation/center_7/"

FS_DATASET=${MAIN_FOLDER}"/input/FreeSurferSD"
OUTPUT_FOLDER=${MAIN_FOLDER}"/output"
GROUPFILE_FOLDER=${MAIN_FOLDER}"/group"


#ID="5b0d1740ef1a5c000f276e72"
#ID="5b0d1744ef1a5c000f276e73"
#ID="5b0d1747ef1a5c000f276e74"
#ID="5b0d174aef1a5c000f276e75"
#ID="5b0d174cef1a5c000f276e76"
#ID="5b0d174eef1a5c000f276e77"
# ID="5b0d1750ef1a5c000f276e78"

# All the data
#ID="5b100d89b0395f0011263592"

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

## Run ENIGMA Shape Analysis
#SCRIPT=${CURRENT_DIR}"/../imaging/eshaoe/build.sh"
#CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
#eval ${CMD}

# Run PLSR Analysis
# CMD="bash "${CURRENT_DIR}"/../PLSR/build.sh "${OUTPUT_FOLDER}" "${ID}
# eval ${CMD}

declare -a ids=(
    "a" 
    "b" 
    "c")
echo "Accessing element 3"${ids[2]}

for id in ${ids[@]}
do
    echo -e ${id}
done