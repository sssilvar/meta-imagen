import os
from os.path import join, dirname

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set environment up
plt.style.use('ggplot')
os.system('clear')


if __name__ == '__main__':
    # Define params
    n_centers = 8
    main_folder = '/home/ssilvari/Documents/temp/data_simulation/'
    aio_folder = join(main_folder, 'all_in_one')

    # Check statistics
    # Get global statistics: gs
    gs = np.load(join(aio_folder, 'output', 'welford', 'welford_final.npz'))
    w_tilde_g = np.load(join(aio_folder, 'output', 'admm', 'w_tilde_iter_9.npz'))['W_tilde']
    plsr_g = np.load(join(aio_folder, 'output', 'plsr', 'plsr.npz'))
    print(plsr_g.keys())


    g_mean = gs['mean']
    g_var = gs['var']
    g_weights = plsr_g['w']
    g_comps = plsr_g['comp']

    # Compare with every local center
    print('MSE Statistics')
    err_mean = []
    err_var = []
    err_w_tilde = []
    for i in range(1, n_centers + 1):
        center_folder = join(main_folder, 'center_%d' % i, 'output')
        # Load local statistics: ls
        ls = np.load(join(center_folder, 'welford', 'welford_final.npz'))
        l_mean = ls['mean']
        l_var = ls['var']
        err_mean.append(((g_mean - l_mean) ** 2).mean())
        err_var.append(((g_var - l_var) ** 2).mean())

        # W_Tilde error
        w_tilde_l = np.load(join(center_folder, 'admm', 'w_tilde_iter_9.npz'))['W_tilde']
        err_w_tilde.append(((w_tilde_g - w_tilde_l) ** 2).mean())

        # PLS components
        plsr = np.load(join(center_folder, 'plsr', 'plsr.npz'))
        l_weights, l_comps = plsr['w'], plsr['comp']

        print('Global: \n%s' % g_comps)
        print('local: \n%s' % l_comps)
        print('\n')



    plt.show()
    
