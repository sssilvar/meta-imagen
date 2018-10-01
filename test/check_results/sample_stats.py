import os
from os.path import join

import pandas as pd


if __name__ == '__main__':
    # Main folder: main_folder
    # Number of centers: n_centers
    n_centers = 4
    main_folder = '/disk/Data/data_simulation/'

    for i in range(1, n_centers + 1):
        # Center folder: cf
        cf = join(main_folder, 'center_%d/output' % i)

        # Common data file: cd_file
        cd_file = join(cf, 'common_data.csv')
        cdf = pd.read_csv(cd_file, index_col=0)
        cdf['Sex'] = cdf['Sex'].astype('category').cat.rename_categories(['Male', 'Female'])

        print('\n\n ======== Information Center %d ========')
        print(cdf.head())
        print('Statistics:')
        print('Mean Age: %s '% cdf['Age'].mean())
        print('Std Age: %s '% cdf['Age'].std())
        print(cdf['Sex'].count())

        


        