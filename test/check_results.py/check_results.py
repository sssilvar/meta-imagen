import os
from os.path import join, dirname

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set environment up
plt.style.use('ggplot')


if __name__ == '__main__':
    # Define params
    n_centers = 8
    main_folder = '/home/ssilvari/Documents/temp/data_simulation/'
    aio_folder = join(main_folder, 'all_in_one')

    # Check statistics
    # Get global statistics: gs
    gs = np.load(join(aio_folder, 'output', 'welford', 'welford_final.npz'))
    g_mean = gs['mean']
    g_var = gs['var']

    # Compare with every local center
    for i in range(1, n_centers + 1):
        center_folder = join(main_folder, 'center_%d' % i, 'output')
        # Load local statistics: ls
        ls = np.load(join(center_folder, 'welford', 'welford_final.npz'))
        l_mean = ls['mean']
        l_var = ls['var']
        print(l_mean[1])
        print(g_mean[1])
        # print(((g_mean - l_mean) ** 2).mean())
        # print(((g_var - l_var) ** 2).mean())

    
