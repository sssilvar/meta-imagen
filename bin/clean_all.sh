#!/bin/bash

WORKDIR=${1-'/disk/Data/data_simulation'}
N_OF_CENTERS=${2-7}

echo " ==== METAIMAGEN CLEANER ==== "
echo -e "\t- Working directory: "${WORKDIR}"\n\t- Number of centers: "${N_OF_CENTERS}

for i in $(seq 1 ${N_OF_CENTERS})
do
    CENTER_FOLDER=${WORKDIR}"/center_"${i}"/output"

    echo "Cleaning center "${i}" ("${CENTER_FOLDER}")"
    eval "rm -rf "${CENTER_FOLDER}"/welford "${CENTER_FOLDER}"/admm "${CENTER_FOLDER}"/plsr "
    eval "rm "${CENTER_FOLDER}"/*_centered.csv "${CENTER_FOLDER}"/*_admm.csv "${CENTER_FOLDER}"/.plsr"
done
