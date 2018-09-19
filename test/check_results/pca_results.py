import os
from os.path import join

import numpy as np
import pandas as pd

from PLSR import PLSR

import seaborn as sns
import matplotlib.pyplot as plt
# plt.style.use('ggplot')
sns.set(color_codes=True)



if __name__ == '__main__':
    # Set up basic stuff
    main_folder = '/disk/Data/data_simulation'
    n_centers = 3

    features = []
    U = []
    WB = []
    for i in range(1, n_centers + 1):
        csv = join(main_folder, 'center_%d' % i, 'output', 'groupfile_features_admm.csv')
        print('[  INFO  ] Loading %s' % csv)
        df = pd.read_csv(csv, index_col=0)
        features.append(df)
            
        # Load PLSR results
        npz_plsr = join(main_folder, 'center_%d' % i, 'output', 'plsr','plsr.npz')
        plsr = np.load(npz_plsr)
        U.append(plsr['comp'][0])
        WB.append(plsr['comp'][1])
    
    df_feats = pd.concat(features, axis=0)

    # ==== Assign labels ===
    # Initialize array
    labels = np.empty(len(df_feats))
    label_names = list(np.empty_like(labels))

    adni_prog = pd.read_csv('https://raw.githubusercontent.com/sssilvar/CSD-AD/master/param/common/adnimerge_conversions_v2.csv', index_col='PTID')
    controls_uk = ['3679417', '4750610', '3907430', '3141907', '5112837', '3475195',
       '4174334', '1496541', '1031176', '3728405', '4478520', '2852289',
       '4159870', '5367099', '4605002', '3203749', '4155810', '1241480',
       '1693795', '4606673', '4816754', '5139990', '5133747', '4108683',
       '3039029', '5817232', '4239395', '2035774', '3985382', '2436654',
       '5340504', '1549892', '2009566', '2546076', '4056050', '4930310',
       '1443931', '2099590', '3721435', '1139817', '3506429', '3095067',
       '3303808', '1159944', '4732188', '2430788', '2519560', '2155568',
       '4476610', '1006400', '3790812', '3985669', '1489425']

    for i, sid in enumerate(df_feats.index):
        if 'HC' in sid:
            labels[i] = 0
            label_names[i] = 'HC-MIRIAD'
        elif 'AD' in sid:
            labels[i] = 4
            label_names[i] = 'AD-MIRIAD'
        elif '_20252' in sid:
            if sid[:-6] in controls_uk:
                label_names[i] = 'HC-UKB'
            else:
                label_names[i] = 'Other-UKB'
        else:
            if any([sid in s for s in adni_prog.index]):
                labels[i] = 2
                label_names[i] = 'MCIc-ADNI'
            else:
                labels[i] = 1
                label_names[i] = 'MCInc-ADNI'

    # Load components
    X = np.vstack(U)
    Y = np.vstack(WB)

    plsr = PLSR(X, Y)
    plsr.Initialize()
    plsr.EvaluateComponents()
    U, V = plsr.GetWeights()

    # Project data and see magic
    E = df_feats.values
    pca_x = E.dot(V)

    # plt.scatter(U[:,0], V[:, 0])  # Relationship between U and V

    # Set markers: HC and AD belong to MIRIAD. MCIc, MCInc, belong to ADNI
    markers = ['o', 'o', 'o', 'x', 'x', 'o']
    palette = {
        'HC-MIRIAD': '#004B99',
        'HC-UKB': '#007DFF',
        'Other-UKB': '#633F00',
        'MCIc-ADNI': '#CC8200',
        'MCInc-ADNI': '#469C0C',
        'AD-MIRIAD': '#AA1500'
    }

    # Plot
    result = pd.DataFrame(pca_x, columns=['PC%d'% (i+1) for i in range(pca_x.shape[1])])
    result['label'] = label_names

    sns.lmplot('PC1', 'PC2', data=result, fit_reg=False,
            scatter_kws={'s': 50},  # Marker size
            hue='label',  # Color
            markers=markers, legend=False,
            palette=palette)
    plt.title('PCA Result')
    # Move the legend to an empty part of the plot
    plt.legend(loc='lower left')


    sns.lmplot('PC2', 'PC3', data=result, fit_reg=False,
            scatter_kws={'s': 40},  # Marker size
            hue='label',  # Color
            markers=markers, legend=False,
            palette=palette)
    plt.title('PCA Result')
    # Move the legend to an empty part of the plot
    plt.legend(loc='lower left')

    # Plot contours
    plt.figure()
    legends = []
    colors = ['Reds', 'Blues', 'Purples', 'Greens', 'Oranges', 'Greys']
    for i, (key, val) in enumerate(palette.items()):
        data = result[result['label'] == key]
        ax = sns.kdeplot(data['PC1'], data['PC2'],
                        n_levels=3,
                        cmap=colors[i], 
                        shade=False, 
                        shade_lowest=False, 
                        alpha=0.8)
        ax.set_label(key)

        # legends.append(key)
    # plt.legend(legends)
    plt.show()

