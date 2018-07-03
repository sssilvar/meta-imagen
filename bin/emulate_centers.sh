#!/usr/bin/env bash

# Run the ENIGMA Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# ++++++++ RUN ALL CENTERS ++++++++
# Declare an array containing all the IDs
declare -a IDS=(
   "5b39f1192b5707000fdd67c8"  # Center 1
   "5b39f1192b5707000fdd67c9"  # Center 2
   "5b39f1192b5707000fdd67ca"  # Center 3
   "5b39f1192b5707000fdd67cb"  # Center 4
   "5b39f1192b5707000fdd67cc"  # Center 5
   "5b39f1192b5707000fdd67cd"  # Center 6
   "5b39f1192b5707000fdd67ce"  # Center 7
   )

for id in 0 1 2 3 4 5 6
do
    # Get id: ID
    ID=${IDS[id]}

    # Print some info
    echo -e "\n\n+++++++++++ MetaImaGen EMULATION CENTER +++++++++++ \n"
    echo -e "[  INFO  ] Processing center "${ID}
#    MAIN_FOLDER="/disk/Data/center_simulation/center_"$((${id} + 1))
    MAIN_FOLDER="/disk/Data/center_simulation/test"

    # Set work directories
    FS_DATASET=${MAIN_FOLDER}"/input"
    OUTPUT_FOLDER=${MAIN_FOLDER}"/output"
    GROUPFILE_FOLDER=${MAIN_FOLDER}"/group"

    echo -e "\n\t\t- Input folder: "${FS_DATASET} \
            "\n\t\t- output Folder: "${OUTPUT_FOLDER} \
            "\n\t\t- groupfile.csv folder: " ${GROUPFILE_FOLDER}

    # Run ENIGMA Shape Analysis
    SCRIPT=${CURRENT_DIR}"/../imaging/eshape/build.sh"
    CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
    eval ${CMD}

    # Run Cortical Shape Analysis
    SCRIPT=${CURRENT_DIR}"/../imaging/cortical_analysis/build.sh"
    CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
    eval ${CMD}

    # Run PLSR Analysis
    CMD="bash "${CURRENT_DIR}"/../PLSR/build.sh "${OUTPUT_FOLDER}" "${ID}
    eval ${CMD}
done