#!/bin/bash

#====FOLDER====
DATA_FOLDER=$1
ID=$2
SERVER=${3-'http://localhost:3300/'}

# Set parameters up
CONTAINER_NAME="admm_client_"${ID}
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
CRE_IMG="docker build -t "${IMG_NAME}" --build-arg proxy="${PROXY}" --build-arg id="${ID}" --build-arg server="${SERVER}" "${CURRENT_DIR}
eval ${CRE_IMG}

echo -e "\n\n[  OK  ] Running container: "${CONTAINER_NAME}
CMD="docker run --name "${CONTAINER_NAME}" --rm -ti -v "${DATA_FOLDER}":/root/data/ "${IMG_NAME}
echo ${CMD}
eval ${CMD}