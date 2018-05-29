#!/usr/bin/env bash

OUTPUT_FOLDER="/user/ssilvari/home/Documents/temp/output"
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CMD="bash "${CURRENT_DIR}"/../PLSR/build.sh "${OUTPUT_FOLDER}
eval ${CMD}