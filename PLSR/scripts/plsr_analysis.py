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
import logging

import requests
import numpy as np
import pandas as pd

# Set root folder
root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root)

from lib.PLSR import PLSR
from lib import api


def plsr_analysis(csv_file_x, csv_file_y, threshold=0.6):
    """
    This function performs the PLSR analysis, and calculates the feature-wise average and standard deviation.
    :param csv_file_x: Path to the csv_file that contains the data for X
    :param csv_file_y: Path to the csv_file that contains the data for Y
    :param threshold: It is a threshold *****
    """

    # Get the work directory from the file path
    print_and_log("[  OK  ] Working directory: %s" % workdir)

    # Load the data
    df_x = pd.read_csv(csv_file_x, index_col=0)
    df_y = pd.read_csv(csv_file_y, index_col=0)
    # df_x = pd.read_hdf(csv_file_x, key='features', index_col=0)
    # df_y = pd.read_hdf(csv_file_y, key='features', index_col=0)

    X = df_x.values
    Y = df_y.values
    print_and_log('[  INFO  ] Matrices info:')
    print_and_log('\t\t- Shape of X: %s' % str(X.shape) + ' | NaN found: %d' % np.count_nonzero(np.isnan(X)))
    print_and_log('\t\t- Shape of Y: %s' % str(Y.shape) + ' | NaN found: %d' % np.count_nonzero(np.isnan(Y)))

    # Start PLS Analysis
    print_and_log('[  INFO  ] Starting PLSR')
    plsr = PLSR(X, Y)
    plsr.Initialize()

    # Evaluate the components and extract the weights
    plsr.EvaluateComponents(threshold)
    comp = plsr.ReturnComponents()
    weights = plsr.GetWeights()

    # Calculate average and standard deviation feature-wise (From the center)
    avgX, stdX, avgY, stdY = plsr.GetStatistics()

    print_and_log('[  INFO  ] Saving data in: %s' % out_dir)
    
    # Save the results
    cid = api.get_client_id()
    out_file = os.path.join(out_dir, 'plsr_%s.npz' % cid)

    np.savez_compressed(
        out_file,
        avx=avgX, avy=avgY,
        stx=stdX, sty=stdY,
        comp=comp, w=weights
    )

    # Upload file
    print_and_log('[  DEBUG  ] Uploading data to: ' + api.get_server_url())
    url = api.get_server_url() + 'upload'
    metadata = {
        'type': 'PLSR',
        'id': api.get_client_id()
    }

    api.upload_file(url, filename=out_file, metadata=metadata)
    
    # Rename to keep the same name in every case
    os.rename(out_file, out_file.replace('_' + cid, ''))


def setup_logger(log_file):
    # ======= SetUp and start logger =======
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def print_and_log(message):
    print(message)
    if 'INFO' in message:
        logger.info(message)
    elif 'WARNING' in message:
        logger.warning(message)
    elif 'ERROR' in message:
        logger.error(message)
    else:
        logger.debug(message)


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

    # Set main dir (log and results are gonna be saved here)
    workdir = os.path.dirname(args.x)
    out_dir = os.path.join(workdir, 'plsr')
    log_file = os.path.join(out_dir, 'plsr.log')

    try:
        os.mkdir(out_dir)
    except IOError:
        print('[  WARNING  ] PLSR folder already exists')

    # Setup logger
    logger = setup_logger(log_file)

    print_and_log("====== PLSR ANALYSIS ======")
    print_and_log("\t X-Data located at: %s" % args.x)
    print_and_log("\t Y-Data located at: %s\n" % args.y)

    try:
        plsr_analysis(csv_file_x=args.x, csv_file_y=args.y)
    except Exception as e:
        # Print exception
        print_and_log('[  ERROR  ] {}'.format(e))
        raise SystemExit

    print_and_log("[  OK  ] DONE!")
