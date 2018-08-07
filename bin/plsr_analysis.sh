#!/usr/bin/env bash

OUTPUT_FOLDER="/disk/Data/data_simulation/center_2/output"
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

HOST="http://ec2-35-167-100-77.us-west-2.compute.amazonaws.com:3300/"

CMD="bash "${CURRENT_DIR}"/../PLSR/build.sh "${OUTPUT_FOLDER}" 5b3383924bab0b42506ff78a "${HOST}
eval ${CMD}