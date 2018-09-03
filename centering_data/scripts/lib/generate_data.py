import os
import argparse

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# bash bin/admm_client.sh /disk/Data/data_simulation/center_1/output 5b3383924bab0b42506ff78a

def clean_previous(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                filename = os.path.join(root, file)
                print('Removing ' + filename)
                os.remove(filename)

def mkdir(folder_path):
    try:
        os.mkdir(folder_path)
    except Exception as e:
        print(e)

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
    n_features = args.nof
    n_cdata = 20
    centers_folder = '/disk/Data/data_simulation'
    # Number of center: n_bunches
    n_bunches = args.centers
    
    # Fix seed for reproducibility
    np.random.seed(42)

    # Delete previous data
    print('[  INFO  ] Cleaning folder...')
    clean_previous(centers_folder)
    aio_folder = os.path.join(centers_folder, 'all_in_one')

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
    plt.savefig(os.path.join(aio_folder, 'output', 'data.pdf'), bbox_inches=None)
    # plt.show()

    # Create folders for 'all in one' and save real W
    mkdir(aio_folder)
    mkdir(os.path.join(aio_folder, 'output'))
    np.savez_compressed(os.path.join(aio_folder, 'output', 'W.npz'), W)

    # Create and save DataFrames
    df_feats = pd.DataFrame(data=feats_data, columns=feats_cols)
    df_feats.to_csv(os.path.join(aio_folder, 'output', 'groupfile_features.csv'))

    df_common = pd.DataFrame(data=common_data, columns=common_cols)
    df_common.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'common_data.csv'))

    
    for i, (f_data, c_data) in enumerate(zip(np.split(feats_data, n_bunches), np.split(common_data, n_bunches))):
        print('Bunch %d shape features: %s | shape common data: %s' % (i, f_data.shape, c_data.shape))
        
        # Create center_i folder
        center_folder = os.path.join(centers_folder, 'center_%d' % (i + 1))
        mkdir(center_folder)
        mkdir(os.path.join(center_folder, 'output'))        

        # Save ith center data
        df_feats = pd.DataFrame(data=f_data, columns=feats_cols)
        df_feats.to_csv(os.path.join(center_folder, 'output', 'groupfile_features.csv'))

        df_common = pd.DataFrame(data=c_data, columns=common_cols)
        df_common.to_csv(os.path.join(center_folder, 'output', 'common_data.csv'))