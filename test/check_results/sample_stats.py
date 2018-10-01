import os
from os.path import join

import pandas as pd
import numpy as np


if __name__ == '__main__':
    # Set up basic stuff
    # Define number of centers: n_centers
    n_centers = 4
    main_folder = '/disk/Data/data_simulation'
    
    # Define and create results folder: results_folder
    results_folder = join(main_folder, 'results')
    os.system('mkdir %s ' % results_folder)

    common = []
    for i in range(1, n_centers + 1):
        # Load Common data
        csv = join(main_folder, 'center_%d' % i, 'output', 'common_data.csv')
        print('[  INFO  ] Loading %s' % csv)
        cdf = pd.read_csv(csv, index_col=0)
        common.append(cdf)

        # If center 1 (MIRIAD) reindex
        if i == 1:
            csv = join(main_folder, 'center_%d' % i, 'output', 'groupfile_features.csv')
            cdf.index = pd.read_csv(csv, index_col=0, usecols=[0]).index

        # Center 4 contains PPMI data
        if i == 4:
            pd_labels = cdf.index.astype(str)

    # Concatenate common dataframes
    df_comm = pd.concat(common, axis=0)
    df_comm.index = df_comm.index.astype(str)
    print(df_comm.head(3))

    # ==== Assign labels ===
    # Initialize array
    labels = np.empty(len(df_comm))
    label_names = list(np.empty_like(labels))

    # Load progressions from MCI to Dementia (MCIc)
    adni_prog = pd.read_csv('https://raw.githubusercontent.com/sssilvar/CSD-AD/master/param/common/adnimerge_conversions_v2.csv', index_col='PTID')
    adni_no_prog = pd.read_csv('https://raw.githubusercontent.com/sssilvar/CSD-AD/master/param/common/adnimerge_MCInc_v2.csv', index_col='PTID')

    # Load remaining diagnosis from adnimerge. Filter: Baseline
    adnimerge = pd.read_csv('https://raw.githubusercontent.com/sssilvar/CSD-AD/master/param/common/adnimerge.csv', index_col='PTID', low_memory=False)
    adnimerge = adnimerge[adnimerge['VISCODE'] == 'bl']

    controls_uk = ['3679417', '4750610', '3907430', '3141907', '5112837', '3475195',
       '4174334', '1496541', '1031176', '3728405', '4478520', '2852289',
       '4159870', '5367099', '4605002', '3203749', '4155810', '1241480',
       '1693795', '4606673', '4816754', '5139990', '5133747', '4108683',
       '3039029', '5817232', '4239395', '2035774', '3985382', '2436654',
       '5340504', '1549892', '2009566', '2546076', '4056050', '4930310',
       '1443931', '2099590', '3721435', '1139817', '3506429', '3095067',
       '3303808', '1159944', '4732188', '2430788', '2519560', '2155568',
       '4476610', '1006400', '3790812', '3985669', '1489425']

    # Dictionary of labels:l
    l = {'HC': 0, 'MCInc': 1, 'MCIc': 2, 'AD': 3, 'PD':4, 'Other': 5}
    
    for i, sid in enumerate(df_comm.index):
        if 'HC' in sid:
            labels[i] = l['HC']
            label_names[i] = 'HC-MIRIAD'

        elif 'AD' in sid:
            labels[i] = l['AD']
            label_names[i] = 'AD-MIRIAD'

        elif sid in pd_labels:
            labels[i] = l['PD']
            label_names[i] = 'PD-PPMI'

        elif '_20252' in sid:
            if sid[:-6] in controls_uk:
                labels[i] = l['HC']
                label_names[i] = 'HC-UKB'
            else:
                labels[i] = l['Other']
                label_names[i] = 'Other-UKB'

        elif any([sid in s for s in adni_prog.index]):
            labels[i] = l['MCIc']
            label_names[i] = 'MCIc-ADNI'

        elif any([sid in s for s in adni_no_prog.index]):
            labels[i] = l['MCInc']
            label_names[i] = 'MCInc-ADNI'

        elif any([sid in s for s in adnimerge.index]):
            dx = adnimerge.loc[sid, 'DX']
            if dx == 'CN':
                labels[i] = l['HC']
                label_names[i] = 'HC-ADNI'
            elif dx == 'Dementia':
                labels[i] = l['AD']
                label_names[i] = 'AD-ADNI'
    
    # Describe datasets
    df_comm['label'] = label_names
    df_comm['label'] = df_comm['label'].astype('category')
    df_comm['Sex'] = df_comm['Sex'].astype('category').cat.rename_categories(['Male', 'Female'])

    for c in df_comm['label'].cat.categories:
        # Get subset of subjects
        df = df_comm.loc[df_comm['label'] == c, :]

        # Print description
        print('\n\n ===== Data description in %s =====' % c)
        print(df.head())
        print('Mean Age: %s' % df['Age'].mean())
        print('Std Age: %s' % df['Age'].std())
        print('Sex counts: %s' % df['Sex'].value_counts())
        print('Total %d' % df.shape[0])



        