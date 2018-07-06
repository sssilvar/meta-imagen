import os

import numpy as np
import pandas as pd


if __name__ == '__main__':
    n = 700
    n_features = 5000
    centers_folder = '/disk/Data/data_simulation'

    whole_data = np.random.normal(1, 1, [n, n_features])
    columns = ['feature %d' %i for i in range(n_features)]

    df = pd.DataFrame(data=whole_data, columns=columns)
    df.to_csv(os.path.join(centers_folder, 'all_in_one', 'output', 'groupfile_features.csv'))

    for i, data in enumerate(np.split(whole_data, 7)):
        print('Bunch %d shape: %s' % (i, data.shape))

        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv(os.path.join(centers_folder, 'center_%d' % (i + 1), 'output', 'groupfile_features.csv'))