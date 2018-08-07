#!/usr/bin/env python3
__author__ = "Santiago Smith, Marco Lorenzi"
__copyright__ = "Copyright 2018, INRIA"
__description__ = """
This code performs a statistical analysis over the files resultant from the ENIGMA Shape pipeline.
It is necessary to have the followin files in order to have a good performance:
    - groupfile_LogJacs.csv
    - groupfile_thick.csv

It is necessary to execute this code per each file as follows:

    python3 plsr_analysis.py -x [path_to_the_X_csv_file] -y [path_to_the_Y_csv_file]
"""

import os
import sys
import argparse

import requests
import numpy as np
import pandas as pd

# Set root folder
root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root)

from lib.PLSR import PLSR
from lib import api


def plsr_analysis(csv_file_x, csv_file_y, threshold=0.01):
    """
    This function performs the PLSR analysis, and calculates the feature-wise average and standard deviation.
    :param csv_file_x: Path to the csv_file that contains the data for X
    :param csv_file_y: Path to the csv_file that contains the data for Y
    :param threshold: It is a threshold *****
    """

    # Get the work directory from the file path
    workdir = os.path.dirname(csv_file_x)
    out_dir = os.path.join(workdir, 'plsr')
    print("[  OK  ] Working directory: ", workdir)

    # Load the data
    df_x = pd.read_csv(csv_file_x, index_col=0)
    df_y = pd.read_csv(csv_file_y, index_col=0)
    # df_x = pd.read_hdf(csv_file_x, key='features', index_col=0)
    # df_y = pd.read_hdf(csv_file_y, key='features', index_col=0)

    X = df_x.values
    Y = df_y.values
    print('[  INFO  ] Matrices info:')
    print('\t\t- Shape of X: ', X.shape, ' | NaN found: ', np.count_nonzero(np.isnan(X)))
    print('\t\t- Shape of Y: ', Y.shape, ' | NaN found: ', np.count_nonzero(np.isnan(Y)))

    # Start PLS Analysis
    print("[  OK  ] Starting PLSR")
    plsr = PLSR(X, Y)
    plsr.Initialize()

    # Evaluate the components and extract the weights
    plsr.EvaluateComponents(threshold)
    comp = plsr.ReturnComponents()
    weights = plsr.GetWeights()

    # Calculate average and standard deviation feature-wise (From the center)
    avgX, stdX, avgY, stdY = plsr.GetStatistics()

    print("\n[  INFO  ] Saving data in: ", out_dir)
    # Save the results
    try:
        os.mkdir(out_dir)
    except IOError:
        pass
    
    cid = api.get_client_id()
    out_file = os.path.join(out_dir, 'plsr_%s.npz' % cid)

    np.savez_compressed(
        out_file,
        avx=avgX, avy=avgY,
        stx=stdX, sty=stdY,
        comp=comp, w=weights
    )

    # Upload file
    print('[  INFO  ] Uploading data to: ' + api.get_server_url())
    url = api.get_server_url() + 'upload'
    metadata = {
        'type': 'PLSR',
        'id': api.get_client_id()
    }

    api.upload_file(url, filename=out_file, metadata=metadata)
    
    # Rename to keep the same name in every case
    os.rename(out_file, out_file.replace('_' + cid, ''))


if __name__ == '__main__':
    csv_file = '/disk/Data/data_simulation/center_1/output/groupfile_features.csv'

    # Deal with the arguments
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-x', metavar='-x',
                        help='Path to the csv_file that contains the data for X',
                        default=csv_file)
    parser.add_argument('-y', metavar='-y',
                        help='Path to the csv_file that contains the data for Y',
                        default=csv_file)
    args = parser.parse_args()

    print("====== PLSR ANALYSIS ======")
    print("\t X-Data located at: ", args.x)
    print("\t Y-Data located at: ", args.y)
    print("\n")

    plsr_analysis(csv_file_x=args.x, csv_file_y=args.y)

    print("[  OK  ] DONE!")
