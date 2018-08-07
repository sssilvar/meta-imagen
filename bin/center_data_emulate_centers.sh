# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HOST="http://ec2-35-167-100-77.us-west-2.compute.amazonaws.com:3300/"

# Declare an array containing all the IDs
declare -a IDS=(
   "5b3383924bab0b42506ff78a"  # Center 1
   "5b3383924bab0b42506ff78b"  # Center 2
   "5b3383924bab0b42506ff78c"  # Center 3
   "5b3383924bab0b42506ff78d"  # Center 4
   "5b3383924bab0b42506ff78e"  # Center 5
   "5b3383924bab0b42506ff78f"  # Center 6
   "5b3383924bab0b42506ff78g"  # Center 7
   )

for id in 0 1 2 3 4 5 6
do
    # Get id: ID
    ID=${IDS[id]}

    # Print some info
    echo -e "\n\n+++++++++++ MetaImaGen EMULATION CENTER +++++++++++ \n"
    echo -e "[  INFO  ] Processing center "${ID}

    # ===== SIMULATION ===== 
    MAIN_FOLDER="/disk/Data/data_simulation/center_"$((${id} + 1))

    # ===== END OF SIMULATION ===== 

    # Set work directories
    FS_DATASET=${MAIN_FOLDER}"/input"
    OUTPUT_FOLDER=${MAIN_FOLDER}"/output"
    GROUPFILE_FOLDER=${MAIN_FOLDER}"/group"

    eval "rm -rf "${OUTPUT_FOLDER}"/welford"
    eval "rm "${OUTPUT_FOLDER}"/groupfile_features_centered.csv"

    echo -e "\n\t\t- Input folder: "${FS_DATASET} \
            "\n\t\t- output Folder: "${OUTPUT_FOLDER} \
            "\n\t\t- groupfile.csv folder: " ${GROUPFILE_FOLDER}

    # Center data
    SCRIPT=${CURRENT_DIR}"/../centering_data/build.sh"
    CMD="bash "${SCRIPT}" "${OUTPUT_FOLDER}" "${ID}" "${HOST}

    SCREEN="tmux new-session -d -s "${ID}" '"${CMD}"'"
    echo ${SCREEN}
    eval ${SCREEN}

done