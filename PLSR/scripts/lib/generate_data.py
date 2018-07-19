import os

import numpy as np
import pandas as pd


if __name__ == '__main__':
    n = 1200
    n_features = 30000
    n_cdata = 20
    centers_folder = '/disk/Data/data_simulation'
    
    # Fix seed for reproducibility
    np.random.seed(42)

    # Generate features data
    print('[  INFO  ] Generating feature data...')
    feats_data = 200 * np.random.normal(10, 4, [n, n_features])
    feats_cols = ['feature %d' % i for i in range(n_features)]

    df_feats = pd.DataFrame(data=feats_data, columns=feats_cols)
    df_feats.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'groupfile_features.csv'))

    # Generate Common data
    print('[  INFO  ] Generating common data...')
    common_data = np.random.normal(50, 20, [n, n_cdata])
    common_cols = ['common_%d' % i for i in range(n_cdata)]

    df_common = pd.DataFrame(data=common_data, columns=common_cols)
    df_common.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'common_data.csv'))

    # Number of center: n_bunches
    n_bunches = 3
    
    for i, (f_data, c_data) in enumerate(zip(np.split(feats_data, n_bunches), np.split(common_data, n_bunches))):
        print('Bunch %d shape features: %s | shape common data: %s' % (i, f_data.shape, c_data.shape))

        # Save ith center data
        df_feats = pd.DataFrame(data=f_data, columns=feats_cols)
        df_feats.to_csv(os.path.join(centers_folder, 'center_%d' % (i + 1), 'output', 'groupfile_features.csv'))

        df_common = pd.DataFrame(data=c_data, columns=common_cols)
        df_common.to_csv(os.path.join(centers_folder, 'center_%d' % (i + 1), 'output', 'common_data.csv'))