#!/bin/bash

# This script builds the docker image with tag sssilvar/eshape:1.0
# To set the proxy use this format: [http://user:pass@proxy_server.com:port/]
# docker build -t sssilvar/eshape_fs:1.0 \
# 	--build-arg proxy=$1\
# 	$(pwd)

# ==== FOLDERS ====
FS_DATASET=$1
OUTPUT_FOLDER=$2
GROUPFILE_FOLDER=$3
PROXY=$4

echo -e "\n\n[  OK  ] Starting ENIGMA Shape analysis"
echo -e "\n\t - FreeSurfer processed data in: "${FS_DATASET}
echo -e "\n\t - Folder that contains groupfile.csv: "${GROUPFILE}
echo -e "\n\t - Results are going to be stored at: "${OUTPUT_FOLDER}


# Set parameters up
GROUPFILE=$GROUPFILE_FOLDER"/groupfile.csv"
CONTAINER_NAME="enigma_shape"
USER="sssilvar"

IMG_NAME=$USER"/"$CONTAINER_NAME
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo "[  OK  ] Stoping container"
STOP_CONT="docker stop "$CONTAINER_NAME
eval $STOP_CONT

echo "[  OK  ] Deleting container"
DEL_CONT="docker rm "$CONTAINER_NAME
eval $DEL_CONT

echo "[  OK  ] Deleting image"
DEL_IMG="docker rmi "$IMG_NAME
eval $DEL_IMG

echo "[  OK  ] Creating the new image: "$IMG_NAME
CRE_IMG="docker build -t "$IMG_NAME" --build-arg proxy="$PROXY" "$CURRENT_DIR
eval $CRE_IMG

echo -e "\n\n[  OK  ] Running container: "$CONTAINER_NAME
cmd="docker run --name "$CONTAINER_NAME" --rm -ti -v "$GROUPFILE_FOLDER":/group/ -v "$FS_DATASET":/input/ -v "$OUTPUT_FOLDER":/output/ "$IMG_NAME
echo $cmd
eval $cmd