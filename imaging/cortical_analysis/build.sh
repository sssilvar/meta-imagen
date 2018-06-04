#!/bin/bash

#====FOLDER====
MAIN_FOLDER="/disk/Data/center_simulation/all_in_one/"


#DATA_FOLDER=$1
DATA_FOLDER=${MAIN_FOLDER}"/input/FreeSurferSD"
GROUP_FOLDER=${MAIN_FOLDER}"/group"
OUTPUT_FOLDER=${MAIN_FOLDER}"/output_cortical"


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
CRE_IMG="docker build -t "${IMG_NAME}" --build-arg proxy="${http_proxy}" "${CURRENT_DIR}
eval ${CRE_IMG}

echo -e "\n\n[  OK  ] Running container: "${CONTAINER_NAME}
CMD="docker run --name "${CONTAINER_NAME}" --rm -ti -v "${DATA_FOLDER}":/input/ -v "${GROUP_FOLDER}":/group/ -v "${OUTPUT_FOLDER}":/output/ "${IMG_NAME}
echo ${CMD}
eval ${CMD}