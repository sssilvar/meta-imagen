import pandas as pd
import numpy as np
from welford import Welford


if __name__ == '__main__':
    all_csv = '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv'
    df = pd.read_csv(all_csv, index_col=0)
    all_stats = {
        'mean': df.mean().values,
        'std': df.std().values
    }

    print('[  INFO  ] Calculating local WF...')
    wf = Welford()

    for i in range(1,8):
        center_csv = '/disk/Data/data_simulation/center_%d/output/groupfile_features.csv' % i
        data = pd.read_csv(center_csv, index_col=0).values

        wf(data)
    stats = {
        'mean': wf.M,
        'std': np.sqrt(wf.S / (wf.k - 1))
    }

    for key, _ in stats.items():
        err = np.mean(np.abs(stats[key] - all_stats[key]))
        print('%s: %f' % (key, err))

    # ==== Compare with distributed results ====
    print('\n\n[  INFO  ] Comparing with distributed version...')
    distributed_wf = '/disk/Data/data_simulation/center_1/output/welford/welford_final.npz'
    dist = dict(np.load(distributed_wf))
    dist['std'] = np.sqrt(dist['var'] / (dist['k'] - 1))

    for key, _ in stats.items():
        err = np.mean(np.abs(stats[key] - dist[key]))
        print('%s: %f' % (key, err))