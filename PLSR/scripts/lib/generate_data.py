import os
import argparse

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# bash bin/admm_client.sh /disk/Data/data_simulation/center_1/output 5b3383924bab0b42506ff78a


if __name__ == '__main__':
    # Deal with the arguments
    parser = argparse.ArgumentParser(description='Generate data for linear regression.')
    parser.add_argument('-n', metavar='observations',
                        help='Number of observations',
                        type=int,
                        default=1600)
    parser.add_argument('-centers', metavar='centers',
                        help='Number of centers',
                        type=int,
                        default=4)
    parser.add_argument('-nof', metavar='features',
                        help='Number of features',
                        type=int,
                        default=30000)
    parser.add_argument('-nf', metavar='noise',
                        help='Noise factor.',
                        type=int,
                        default=1)
    args = parser.parse_args()
    
    # ==== START ====
    n = args.n
    n_features = 30000
    n_cdata = 20
    centers_folder = '/disk/Data/data_simulation'
    # Number of center: n_bunches
    n_bunches = args.centers
    
    # Fix seed for reproducibility
    np.random.seed(42)

    # Generate Common data
    print('[  INFO  ] Generating common data...')
    common_data = np.random.normal(45, 10, [n, n_cdata])
    common_cols = ['common_%d' % i for i in range(n_cdata)]
    
    # Generate W
    W = np.random.normal(5, 1, [n_cdata, n_features]) * 5

    # Generate features data
    print('[  INFO  ] Generating feature data...')
    feats_data = common_data.dot(W) + args.nf * np.random.normal(0, 50, [n, n_features])
    feats_cols = ['feature %d' % i for i in range(n_features)]

    # Plot the results
    plt.scatter(feats_data[0], common_data.dot(W)[0])
    plt.show()

    # create DataFrames
    df_feats = pd.DataFrame(data=feats_data, columns=feats_cols)
    df_feats.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'groupfile_features.csv'))

    df_common = pd.DataFrame(data=common_data, columns=common_cols)
    df_common.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'common_data.csv'))

    
    for i, (f_data, c_data) in enumerate(zip(np.split(feats_data, n_bunches), np.split(common_data, n_bunches))):
        print('Bunch %d shape features: %s | shape common data: %s' % (i, f_data.shape, c_data.shape))

        # Save ith center data
        df_feats = pd.DataFrame(data=f_data, columns=feats_cols)
        df_feats.to_csv(os.path.join(centers_folder, 'center_%d' % (i + 1), 'output', 'groupfile_features.csv'))

        df_common = pd.DataFrame(data=c_data, columns=common_cols)
        df_common.to_csv(os.path.join(centers_folder, 'center_%d' % (i + 1), 'output', 'common_data.csv'))