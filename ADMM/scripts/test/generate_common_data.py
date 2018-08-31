import os
import numpy as np
import pandas as pd

if __name__ == '__main__':
    output_folder = '/disk/Data/data_simulation/all_in_one/output'
    features_file = '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv'

    df = pd.read_csv(features_file, index_col=0)
    n, d_feats = df.shape

    data = {}
    for i in range(20):
        mean = np.random.randint(1, 80)
        std = np.random.randint(1, 30)

        data['common_%d' %i] = np.random.normal(mean, std, n)
    
    df_common = pd.DataFrame(data)
    df_common.to_csv(os.path.join(output_folder, 'common_data.csv'))

