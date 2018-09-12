import os
from os.path import join

import numpy as np
import pandas as pd


if __name__ == '__main__':
    # Set up basic stuff
    main_folder = '/disk/Data/data_simulation'
    n_centers = 2

    features = []
    plsr = []
    for i in range(1, n_centers + 1):
        csv = join(main_folder, 'center_%d' % i, 'output', 'groupfile_features.csv')
        print('[  INFO  ] Loading %s' % csv)
        df = pd.read_csv(csv, index_col=0)
        features.append(df)
            
        # Load PLSR results
        npz_plsr = join(main_folder, 'center_%d' % i, 'output', 'plsr','plsr.npz')
        plsr.append(np.load(npz_plsr))
    
    df_feats = pd.concat(features, axis=0)

    # ==== Assign labels ===
    # Initialize array
    labels = np.empty(len(df_feats))
    label_names = list(np.empty_like(labels))

    adni_prog = pd.read_csv('https://raw.githubusercontent.com/sssilvar/CSD-AD/master/param/data_df.csv', index_col='folder')

    for i, sid in enumerate(df_feats.index):
        if 'HC' in sid:
            labels[i] = 0
            label_names[i] = 'HC'
        elif 'AD' in sid:
            labels[i] = 4
            label_names[i] = 'AD'
        else:
            labels[i] = adni_prog.loc[sid, 'target'] + 1
            label_names[i] = adni_prog.loc[sid, 'dx_group']

    # Load components
    print(plsr)
    print(plsr[0])

