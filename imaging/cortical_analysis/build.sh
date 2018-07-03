#!/bin/bash

# ==== FOLDERS ====
FS_DATASET=$1
OUTPUT_FOLDER=$2
GROUPFILE_FOLDER=$3
PROXY=$4

echo -e "\n\n[  OK  ] Starting Cortical Shape analysis"
echo -e "\n\t - FreeSurfer processed data in: "${FS_DATASET}
echo -e "\n\t - Folder that contains \"groupfile.csv\": "${GROUPFILE_FOLDER}
echo -e "\n\t - Results are going to be stored at: "${OUTPUT_FOLDER}
echo -e "\n\n\n"


# Set parameters up
CONTAINER_NAME="cortical_tk_jac"
USER="sssilvar"

IMG_NAME=$USER"/"${CONTAINER_NAME}
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "\n\n[  OK  ] Stoping container"
STOP_CONT="docker stop "${CONTAINER_NAME}
eval ${STOP_CONT}

echo -e "\n\n[  OK  ] Deleting container"
DEL_CONT="docker rm "${CONTAINER_NAME}
eval ${DEL_CONT}

echo -e "\n\n[  OK  ] Deleting image"
DEL_IMG="docker rmi "${IMG_NAME}
eval ${DEL_IMG}

echo -e "\n\n[  OK  ] Creating the new image: "${IMG_NAME}
CRE_IMG="docker build -t "${IMG_NAME}" --build-arg proxy="${PROXY}" "${CURRENT_DIR}
eval ${CRE_IMG}

echo -e "\n\n[  OK  ] Running container: "${CONTAINER_NAME}
CMD="docker run --name "${CONTAINER_NAME}" --rm -ti -v "${FS_DATASET}":/input/ -v "${GROUPFILE_FOLDER}":/group/ -v "${OUTPUT_FOLDER}":/output/ "${IMG_NAME}
echo ${CMD}
eval ${CMD}