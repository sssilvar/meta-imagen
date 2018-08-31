#!/usr/bin/env bash

echo "[  OK  ] Starting cortical feature extraction"
eval "python /root/scripts/pipeline.py"

eval "chmod -R 777 /output"

