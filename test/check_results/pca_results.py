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
    n_centers = 2

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

    for i, sid in enumerate(df_feats.index):
        if 'HC' in sid:
            labels[i] = 0
            label_names[i] = 'HC'
        elif 'AD' in sid:
            labels[i] = 4
            label_names[i] = 'AD'
        else:
            if any([sid in s for s in adni_prog.index]):
                labels[i] = 2
                label_names[i] = 'MCIc'
            else:
                labels[i] = 1
                label_names[i] = 'MCInc'

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

    plt.scatter(U[:,0], V[:, 0])

    # Set markers: HC and AD belong to MIRIAD. MCIc, MCInc, belong to ADNI
    markers = ['o', 'o', 'x', 'x']
    palette=dict(HC="#004B99", MCInc="#469C0C", MCIc="#CC8200", AD="#AA1500")

    # Plot
    result = pd.DataFrame(pca_x, columns=['PC%d'% (i+1) for i in range(pca_x.shape[1])])
    result['label'] = label_names

    sns.lmplot('PC1', 'PC2', data=result, fit_reg=False,
            scatter_kws={'s': 40},  # Marker size
            hue='label',  # Color
            markers=markers, legend=False,
            palette=palette,
            shade=True)
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

    plt.show()

