#!/usr/bin/env bash

# Run the ENIGMA Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved

# ==== FOLDERS ====
WORKDIR=${1-'/disk/Data/data_simulation'}
N_OF_CENTERS=${2-7}
SERVER=${3-"http://ec2-35-167-100-77.us-west-2.compute.amazonaws.com:3300/"}

# FS_DATASET=${MAIN_FOLDER}"/input/FreeSurferSD"
# OUTPUT_FOLDER=${MAIN_FOLDER}"/output"
# GROUPFILE_FOLDER=${MAIN_FOLDER}"/group"

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Declare an array containing all the IDs
declare -a IDS=(
    "5ba1049b4a24c500103da1c0"
    "5ba1049c4a24c500103da1c2"
    "5ba1049c4a24c500103da1c1"
    "5ba1049b4a24c500103da1bf"
    "5ba1049b4a24c500103da1be"
    "5ba1049b4a24c500103da1bd"
    "5ba1049a4a24c500103da1bb"
    "5ba1049a4a24c500103da1bc"
   )

# Clean Everything
# eval "bash "${CURRENT_DIR}"/clean_all.sh "${WORKDIR}" "${N_OF_CENTERS}

for i in $(seq 1 ${N_OF_CENTERS})
do
    # Assign current id: ID
    ID=${IDS[$((${i} - 1))]}

    # Set current folders
    CENTER_FOLDER=${WORKDIR}"/center_"${i}
    FS_DATASET=${CENTER_FOLDER}"/input"
    OUTPUT_FOLDER=${CENTER_FOLDER}"/output"
    GROUPFILE_FOLDER=${CENTER_FOLDER}"/group"

    # Print some info
    echo -e "\n\n\nCenter "${i}" | ID: "${ID}
    echo -e "\n\t\t- Input folder: "${FS_DATASET} \
            "\n\t\t- output Folder: "${OUTPUT_FOLDER} \
            "\n\t\t- groupfile.csv folder: " ${GROUPFILE_FOLDER} \
            "\n\t\t- API server folder: " ${SERVER}
    
    # Run center
    SCRIPT=${CURRENT_DIR}"/run_pipeline.sh"
    CMD="bash "${SCRIPT}" "${CENTER_FOLDER}" "${ID}" "${SERVER}

    DAEMON="tmux new-session -d -s "${ID}" '"${CMD}"'"
    echo ${DAEMON}
    eval ${DAEMON}
    eval "sleep 10"
done