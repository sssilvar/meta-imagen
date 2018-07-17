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
   "5b3de1c45ee3ca00100bb751"  # Center 1
   "5b3de1c65ee3ca00100bb752"  # Center 2
   "5b3de1c85ee3ca00100bb753"  # Center 3
   "5b3de1c95ee3ca00100bb754"  # Center 4
   "5b3de1cb5ee3ca00100bb755"  # Center 5
   "5b3de1cd5ee3ca00100bb756"  # Center 6
   "5b3de1ce5ee3ca00100bb757"  # Center 7
   )

for id in 0 #1 2 3 4 5 6
do
    # Get id: ID
    ID=${IDS[id]}

    # Print some info
    echo -e "\n\n+++++++++++ MetaImaGen EMULATION CENTER +++++++++++ \n"
    echo -e "[  INFO  ] Processing center "${ID}
    # MAIN_FOLDER="/disk/Data/center_simulation/center_"$((${id} + 1))
    # MAIN_FOLDER="/disk/Data/center_simulation/test" # For the whole data

    # ===== SIMULATION ===== 
    # MAIN_FOLDER="/disk/Data/data_simulation/center_"$((${id} + 1))
    MAIN_FOLDER="/disk/Data/data_simulation/all_in_one" # For the whole data
    # ===== END OF SIMULATION ===== 

    # Set work directories
    FS_DATASET=${MAIN_FOLDER}"/input"
    OUTPUT_FOLDER=${MAIN_FOLDER}"/output"
    GROUPFILE_FOLDER=${MAIN_FOLDER}"/group"

    echo -e "\n\t\t- Input folder: "${FS_DATASET} \
            "\n\t\t- output Folder: "${OUTPUT_FOLDER} \
            "\n\t\t- groupfile.csv folder: " ${GROUPFILE_FOLDER}

    # # Run ENIGMA Shape Analysis
    # SCRIPT=${CURRENT_DIR}"/../imaging/eshape/build.sh"
    # CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
    # eval ${CMD}

    # # Run Cortical Shape Analysis
    # SCRIPT=${CURRENT_DIR}"/../imaging/cortical_analysis/build.sh"
    # CMD="bash "${SCRIPT}" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
    # eval ${CMD}

    # # Run PLSR Analysis
    # CMD="bash "${CURRENT_DIR}"/../PLSR/build.sh "${OUTPUT_FOLDER}" "${ID}
    # eval ${CMD}

    # # Run ADMM optimization
    # CMD="bash "${CURRENT_DIR}"/../ADMM/build.sh "${OUTPUT_FOLDER}" "${ID}
    # eval ${CMD}
done