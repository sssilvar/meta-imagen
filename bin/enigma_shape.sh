#!/bin/bash

# Run the ENIGMA Shape analysis over a FreeSurfer processed dataset (with recon-all)
# map the /group folder to the foder where the groupfile.csv is located in the local
# map the /input foldet to the dataset processed
# map the /output folder where you wnat the results to be saved
# 
# Example:
# 
# docker run -it \
# 	-v <groupfile_csv_folder>:/group \
# 	-v <dataset_folder>:/input \
# 	-v <output_folder>:/output \
# 	sssilvar/eshape_fs /group/groupfile.csv /input /output

# docker run -it \
# 	-v /home/sssilvar/Documents/:/group \
# 	-v /home/sssilvar/Documets/dataset/:/input \
# 	-v /home/sssilvar/Documets/output:/output \
# 	sssilvar/eshape_fs:1.0 /group/groupfile.csv /input /output


# ==== FOLDERS ====
FS_DATASET=/home/sssilvar/Documents/dataset/FreeSurferSD
OUTPUT_FOLDER=/home/sssilvar/Documents/output_docker
GROUPFILE_FOLDER=/home/sssilvar/Documents/group

# Get current dir
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT=$CURRENT_DIR/imaging/build.sh

CMD="bash "$SCRIPT" "${FS_DATASET}" "${OUTPUT_FOLDER}" "${GROUPFILE_FOLDER}" "$1
eval $CMD