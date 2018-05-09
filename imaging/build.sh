#!/bin/bash

# This script builds the docker image with tag sssilvar/eshape:1.0
# To set the proxy use this format: [http://user:pass@proxy_server.com:port/]
# docker build -t sssilvar/eshape_fs:1.0 \
# 	--build-arg proxy=$1\
# 	$(pwd)

# Set parameters up
CONTAINER_NAME="enigma_shape"
USER="sssilvar"
PROXY=$1

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

echo "[  OK  ] Running container: "$CONTAINER_NAME
cmd="docker run --name "$CONTAINER_NAME" -ti "$IMG_NAME
echo $cmd
eval $cmd