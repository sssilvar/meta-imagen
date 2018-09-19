import os
from os.path import join

import numpy as np
import pandas as pd

from PLSR import PLSR

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from sklearn.mixture import GMM


# plt.style.use('ggplot')
sns.set(color_codes=True)


def draw_ellipse(position, covariance, ax=None, **kwargs):
    """Draw an ellipse with a given position and covariance"""
    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    # Draw the Ellipse
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))


def plot_gmm(gmm, X, label=True, ax=None):
    ax = ax or plt.gca()
    labels = gmm.fit(X).predict(X)
    if label:
        ax.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='viridis', zorder=2)
    else:
        # ax.scatter(X[:, 0], X[:, 1], s=40, zorder=2)
        pass
    ax.axis('equal')
    
    w_factor = 0.3 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covars_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)



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
    # markers = ['o', 'o', 'o', 'x', 'x', 'o']
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

    # Filter classes
    query = 'label == "HC-MIRIAD" or ' + \
            'label == "HC-UKB" or ' + \
            'label == "Other-UKB" or ' + \
            'label == "AD-MIRIAD"'
    res_fil = result.query(query)

    sns.lmplot('PC1', 'PC2', data=res_fil, fit_reg=False,
            scatter_kws={'s': 50},  # Marker size
            hue='label',  # Color
            # markers=markers, 
            legend=False,
            palette=palette)
    plt.title('PCA Result')
    # Move the legend to an empty part of the plot
    plt.legend(loc='lower left')
    plt.axis('equal')


    # sns.lmplot('PC1', 'PC3', data=res_fil, fit_reg=False,
    #         scatter_kws={'s': 40},  # Marker size
    #         hue='label',  # Color
    #         # markers=markers, 
    #         legend=False,
    #         palette=palette)
    # plt.title('PCA Result')
    # # Move the legend to an empty part of the plot
    # plt.legend(loc='lower left')

    # # Plot contours
    # plt.figure()
    # legends = []
    # # colors = ['Reds', 'Blues', 'Purples', 'Greens', 'Oranges', 'Greys']
    # colors = ['Blues', 'GnBu', 'Greys', 'Purples', 'Greens', 'Reds']
    # x_c = [-18, 95, 100, 18, -80, -150]
    # y_c = [95, 79, 36, 0, 75, 48]
    # for i, (key, val) in enumerate(palette.items()):
    #     data = result[result['label'] == key]
    #     ax = sns.kdeplot(data['PC1'], data['PC2'],
    #                     n_levels=2,
    #                     alpha=0.8,
    #                     cmap=colors[i], 
    #                     shade=False, 
    #                     shade_lowest=False)
    #     col = sns.color_palette(colors[i])[-2]
    #     ax.text(x_c[i], y_c[i], key, size=16, color=col)
    # plt.xlim(-215, 215)
    # plt.ylim(-150, 150)
    
    # plt.figure()
    # x_c = [34, 120, 40, -22, -90, -110]
    # y_c = [40, 28, -30, -35, -50, -9]
    # for i, (key, val) in enumerate(palette.items()):
    #     data = result[result['label'] == key]
    #     ax = sns.kdeplot(data['PC1'], data['PC3'],
    #                     n_levels=2,
    #                     alpha=0.8,
    #                     cmap=colors[i], 
    #                     shade=False, 
    #                     shade_lowest=False)
    #     col = sns.color_palette(colors[i])[-2]
    #     ax.text(x_c[i], y_c[i], key, size=16, color=col)
    #     # ax.text(x_c[i], y_c[i], key, size=16, color=col)
    # plt.xlim(-215, 215)
    # plt.ylim(-100, 75)


    # ==== GMM ====
    Y = result['label'].astype('category').cat.codes
    X = result.loc[:, ['PC1', 'PC2']].values
    
    gmm = GMM(n_components=4, random_state=42)
    gmm.fit(X)
    
    w_factor = 0.3 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covars_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)

    plt.figure()
    plot_gmm(gmm, X)

    plt.show()

