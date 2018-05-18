import os
import sys

import numpy as np


# Set root folder
root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root)

from lib.PLSR import PLSR


if __name__ == '__main__':
    n_subjects = 20
    n_features = 20

    data = []
    for i in range(1, n_features):
        wise_stats = np.random.normal(i, 1, n_subjects)
        data.append(wise_stats)

    data = np.array(data)

    # for i in data.T:
    #     print(i.mean())
    #     print(i.std())

    # Start PLS Analysis
    plsr = PLSR(data, data)
    plsr.Initialize()

    # Evaluate the components and extract the weights
    plsr.EvaluateComponents(0.01)
    comp = plsr.ReturnComponents()
    weights = plsr.GetWeights()

    # Calculate average and standard deviation feature-wise
    avgX, stdX, avgY, stdY = plsr.GetStatistics()







