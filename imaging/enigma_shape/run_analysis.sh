#!/bin/bash

echo -e "\n\n[  OK  ] Starting ENIGMA Shape analysis"
CMD="./root/enigma_shape/shape_group_run.sh /group/groupfile.csv /input/ /output/"
eval $CMD

echo -e "[  OK  ] End of the ENIGMA Shape analysis\n\n"
eval "ls /output"
eval "chmod 766 -R /output"