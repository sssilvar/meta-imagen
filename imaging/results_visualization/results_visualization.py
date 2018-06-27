import os

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

import matplotlib.pyplot as plt
plt.style.use('ggplot')


if __name__ == '__main__':
    main_folder = '/user/ssilvari/home/Documents'
    csv_features = main_folder + '/output/output_docker_un/groupfile_LogJacs.csv'

    output_folder = main_folder + '/output/output_docker_un/shape_stats/test'
    atlas_folder = main_folder + '/Docker/meta-imagen/imaging/eshape/enigma_shape/MedialDemonsShared/atlas'
    csv_groupfile = '/disk/Data/center_simulation/all_in_one/group/groupfile.csv'

    # Software params
    ccbbm = '/user/ssilvari/home/Documents/Docker/meta-imagen/imaging/eshape/enigma_shape/MedialDemonsShared/bin/ccbbm'
    rois = [10, 11, 12, 13, 17, 18, 26, 49, 50, 51, 52, 53, 54, 58]

    # Read results
    df = pd.read_csv(csv_features, index_col=0)
    df_gf = pd.read_csv(csv_groupfile)
    print('\t\t- Data dimensions: ', np.shape(df.values))

    # Extract classes
    mcic_subjects = df_gf.loc[df_gf['dx'] == 'MCIc']['subj']
    mcinc_subjects = df_gf.loc[df_gf['dx'] == 'MCInc']['subj']

    print('[  OK  ] Starting t-test')
    for roi in rois:
        # Initialize statistics: class 1 (c1) and class 2 (c2)
        t_stats = []
        p_vals = []

        # Set names of the current files
        atlas_file = os.path.join(atlas_folder, 'atlas_%d.m' % roi)
        df_filtered = df.loc[:, df.columns.str.find('_' + str(roi) + '_').astype(bool)]

        print('[  INFO  ] Processing ROI - %d \n'
              '\t Atlas file: %s\n'
              '\t Data File: %s' % (roi, atlas_file, csv_features))
        for col in df_filtered:
            t, p = ttest_ind(df_filtered.loc[mcinc_subjects, col], df_filtered.loc[mcic_subjects, col])
            t_stats.append(t)
            p_vals.append(p)

        t_file = os.path.join(output_folder, 't_stats_thick_%d' % roi)
        p_file = os.path.join(output_folder, 'p_value_thick_%d' % roi)

        stats_files = [t_file, p_file]
        stats_arr = [t_stats, p_vals]

        for i, stat_file in enumerate(stats_files):

            if i == 0:
                range = '-10 10'
            elif i == 1:
                range = '-1 0 -0.05 0'

            # Save RAW file
            (-np.array(stats_arr[i])).tofile(stat_file + '.raw')

            # arr = np.fromfile(stat_file + '.raw')
            # plt.hist(arr)
            # plt.show()

            # Convert RAW to mesh (*.m)
            cmd = ccbbm + ' -color_attribute ' + atlas_file + ' ' + stat_file + '.raw ' + stat_file + '.m ' + range
            # cmd = ccbbm + ' -color_hot_cold ' + atlas_file + ' ' + \
            #       stat_file + '.raw ' + stat_file + '.m ' + range + ' -full_range'
            print(cmd)
            os.system(cmd)

            # Convert mesh to obj
            cmd = ccbbm + ' -mesh2obj ' + stat_file + '.m ' + stat_file + '.obj'
            print(cmd)
            os.system(cmd)
