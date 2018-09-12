import os
from os.path import join

import numpy as np
import pandas as pd


if __name__ == '__main__':
    # Set up basic stuff
    main_folder = '/disk/Data/data_simulation'
    n_centers = 2

    features = []
    for i in range(1, n_centers + 1):
        csv = join(main_folder, 'center_%d' % i, 'output', 'groupfile_features.csv')
        df = pd.read_csv(csv, index_col=0)
        features.append(df)
    df_feats = pd.concat(features, axis=0)

