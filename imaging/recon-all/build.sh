#!/bin/bash

# This script builds the docker image with tag sssilvar/eshape:1.0
# To set the proxy use this format: [http://user:pass@proxy_server.com:port/]
# docker build -t sssilvar/eshape_fs:1.0 \
# 	--build-arg proxy=$1\
# 	$(pwd)

## ==== FOLDERS ====
#DATASET_FOLDER=$1
#OUTPUT_FOLDER=$2
#PROXY=$4

#=== Testing ===
DATASET_FOLDER="/user/ssilvari/home/Documents/Data/data_test"
OUTPUT_FOLDER="/user/ssilvari/home/Documents/Data/data_test_converted"
PROXY=""

echo -e "\n\n[  OK  ] Starting FreeSurfer RECON-ALL analysis"
echo -e "\n\t - Folder containing subjects to be processed: "${DATASET_FOLDER}
echo -e "\n\t - Results are going to be stored at: "${OUTPUT_FOLDER}
echo -e "\n\n\n"


# Set parameters up
CONTAINER_NAME="recon_all"
USER="sssilvar"

IMG_NAME=${USER}"/"${CONTAINER_NAME}
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
cmd="docker run --name "${CONTAINER_NAME}" --rm -ti -v "${DATASET_FOLDER}":/input/ -v "${OUTPUT_FOLDER}":/output/ "${IMG_NAME}
echo ${cmd}
eval ${cmd}