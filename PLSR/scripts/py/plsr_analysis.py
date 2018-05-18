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
root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root)

from lib.PLSR import PLSR


def plsr_analysis(csv_file_x, csv_file_y, threshold=0.01):
    """
    This function performs the PLSR analysis, and calculates the feature-wise average and standard deviation.
    :param csv_file_x: Path to the csv_file that contains the data for X
    :param csv_file_y: Path to the csv_file that contains the data for Y
    :param threshold: It is a threshold *****
    """

    # Get the work directory from the file path
    workdir = os.path.dirname(csv_file)
    out_dir = os.path.join(workdir, 'plsr')
    print("[  OK  ] Working directory: ", workdir)

    # Load the data
    df_x = pd.read_csv(csv_file_x, index_col=0)
    df_y = pd.read_csv(csv_file_y, index_col=0)

    X = df_x.values
    Y = df_y.values

    # Start PLS Analysis
    print("[  OK  ] Starting PLSR")
    plsr = PLSR(X, Y)
    plsr.Initialize()

    # Evaluate the components and extract the weights
    plsr.EvaluateComponents(threshold)
    comp = plsr.ReturnComponents()
    weights = plsr.GetWeights()

    # Calculate average and standard deviation feature-wise
    avgX, stdX, avgY, stdY = plsr.GetStatistics()

    print("\nSaving data in: ", out_dir)
    # Save the results
    try:
        os.mkdir(out_dir)
    except IOError:
        pass
    ext = '.npz'
    out_file = os.path.join(out_dir, 'plsr_results' + ext)

    np.savez(
        out_file,
        avx=avgX, avy=avgY,
        stx=stdX, sty=stdY,
        comp=comp, w=weights
    )

    report = ("[  OK  ] REPORT: \n"
              "\t Data dimensions (shape):\n"
              "\t avgX: %s\n"
              "\t stdX: %s\n\n"
              "\t avgY: %s\n"
              "\t stdY: %s\n\n"
              "\t Components: %s\n"
              "\t Weights: %s\n") % (avgX.shape, stdX.shape, avgY.shape, stdY.shape, np.shape(comp), np.shape(weights))
    print(report)

    # Check the data obtained:
    t = np.load(out_file)

    report = ("[  OK  ] REPORT (checking from files): \n"
              "\t Data dimensions (shape):\n"
              "\t avgX: %s\n"
              "\t stdX: %s\n\n"
              "\t avgY: %s\n"
              "\t stdY: %s\n\n"
              "\t Components: %s\n"
              "\t Weights: %s\n") % \
             (t['avx'].shape, t['stx'].shape, t['avy'].shape, t['sty'].shape,
              np.shape(t['comp']), np.shape(t['w']))
    print(report)


if __name__ == '__main__':
    csv_file = '/user/ssilvari/home/Documents/temp/output/groupfile_thick.csv'

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

    print("[  OK  ] DONE")
