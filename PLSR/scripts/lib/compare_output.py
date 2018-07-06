import os

import numpy as np

if __name__ == '__main__':
    npz_all_data = '/disk/Data/data_simulation/results_npz/wf_all.npz'
    npz_distributed_data = '/disk/Data/data_simulation/results_npz/wf_distributed.npz'

    npa = np.load(npz_all_data)
    npd = np.load(npz_distributed_data)

    for key, _ in npa.items():
        if 'Std' in key or "Avg" in key:
            print('Mean squared error %.2f' % np.mean(np.abs(npa[key] - npd[key]) ** 2))