import os
import sys
import argparse

import numpy as np
import pandas as pd

# Set root folder
root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(root)

from lib.welford import Welford

if __name__ == '__main__':
    real_mean = 3.45
    realt_std = 0.8

    # Generate random data
    data = np.random.normal(real_mean, realt_std, [30000, 30])

    print("Data shape: ", data.shape)
    print("Real Mean: ", data.mean())
    print("Real STD: ", data.std())

    n = 100
    split = np.split(data, n)

    # Start the iterative calculation
    avg = []
    std = []
    wf_arr = []

    for i in range(n):
        data_batch = split[i]
        wf = Welford()
        for d in data_batch.T:
            wf(d)
        avg.append(wf.mean)
        std.append(wf.std)

    #     wf(data_batch)
    #
    # print(wf)




