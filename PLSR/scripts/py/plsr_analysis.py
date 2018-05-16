#!/usr/bin/env python3
"""
This code performs a statistical analysis over the files resultant from the ENIGMA Shape pipeline.
It is necessary to have the followin files in order to have a good performance:
    - groupfile_LogJacs.csv
    - groupfile_thick.csv

It is necessary to execute this code per each file as follows:

    python3 plsr_analysis.py [path_to_the_X_csv_file] [path_to_the_Y_csv_file]
"""

__author__ = "Santiago Smith, Marco Lorenzi"
__copyright__ = "Copyright 2018, INRIA"


import os
import sys

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
    plsr = PLSR(X, Y)
    plsr.Initialize()

    # Evaluate the components and extract the weights
    plsr.EvaluateComponents(threshold)
    comp = plsr.ReturnComponents()
    weights = plsr.GetWeights()

    # Calculate average and standard deviation feature-wise
    avgX, stdX, avgY, stdY = plsr.GetStatistics()

    # Save the results
    try:
        os.mkdir(out_dir)
    except IOError:
        pass
    np.save(os.path.join(out_dir, 'avgX'), avgX)
    np.save(os.path.join(out_dir, 'avgY'), avgY)
    np.save(os.path.join(out_dir, 'stdX'), stdX)
    np.save(os.path.join(out_dir, 'stdY'), stdY)

    np.save(os.path.join(out_dir, 'components'), comp)
    np.save(os.path.join(out_dir, 'weights'), weights)


if __name__ == '__main__':
    csv_file = '/user/ssilvari/home/Documents/temp/output/groupfile_thick.csv'

    plsr_analysis(csv_file_x=csv_file, csv_file_y=csv_file)


