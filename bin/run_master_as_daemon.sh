# ==== FOLDERS ====
WORKDIR=${1-'/disk/Data/data_simulation/all_in_one'}
SERVER=${2-"http://ec2-52-33-192-188.us-west-2.compute.amazonaws.com:3300/"}
ID=${3-"5b894d130f81e6000f237d22"}


# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get main folders
FS_DATASET=${CENTER_FOLDER}"/input"
OUTPUT_FOLDER=${CENTER_FOLDER}"/output"
GROUPFILE_FOLDER=${CENTER_FOLDER}"/group"

# Print some info
echo -e "\n\n\n MAIN CENTER | ID: "${ID}
echo -e "\n\t\t- Input folder: "${FS_DATASET} \
        "\n\t\t- output Folder: "${OUTPUT_FOLDER} \
        "\n\t\t- groupfile.csv folder: " ${GROUPFILE_FOLDER} \
        "\n\t\t- API server folder: " ${SERVER}

# Run center
SCRIPT=${CURRENT_DIR}"/run_pipeline.sh"
CMD="bash "${SCRIPT}" "${CENTER_FOLDER}" "${ID}" \""${SERVER}"\""

DAEMON="tmux new-session -d -s "${ID}" '"${CMD}"'"
echo ${DAEMON}
eval ${DAEMON}
