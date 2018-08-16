import os
import sys

import numpy as np
import pandas as pd

from sklearn.covariance import EmpiricalCovariance
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSSVD, PLSRegression

current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)
sys.path.append(current_dir)

from PLSR import PLSR

if __name__ == '__main__':
    # Initial params
    n = 300
    n_x = 10000
    n_y = 35000
    np.random.seed(42)
    os.system('clear')

    # Create X and W matrices
    X = np.random.normal(size=[n, n_x])
    Y = np.random.normal(size=[n, n_y])
    
    cols_x = [str(i) for i in range(n_x)]
    dfx = pd.DataFrame(X, columns=cols_x)

    # Scalate
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    Y = scaler.fit_transform(Y)

    # ####################################
    # PLSR - Marco
    # ####################################
    plsr = PLSR(X, Y)
    plsr.Initialize()
    plsr.EvaluateComponents()
    weights = plsr.GetWeights()
    comps = plsr.ReturnComponents()
    print('Covariance X (XX\'):\n %s' % X.dot(X.T))
    print('Covariance X (plsr):\n %s' % plsr._covX)

    print('Covariance X (numpy):\n %s' % np.cov(X, rowvar=False))
    print('Covariance X (pandas):\n %s' % dfx.cov().values)

    cov = EmpiricalCovariance(assume_centered=True)
    cov.fit(X)

    print('Covariance X (sklearn):\n %s' % cov.covariance_)
    
    

    # print('weigths 0:\n %s' % weights[0])
    # print('weigths 1:\n %s' % weights[1])

    # print('Y Scores:\n %s' % comps[0])
    # print('Components Y:\n %s' % comps[1])

    # ####################################
    # PLSR - SKLEARN
    # ####################################
    # print('\n\nPLS-SVD')
    # plsr = PLSSVD(n_components=2, scale=False)
    # plsr.fit(X,Y)
    # print('X Weigths: \n%' % plsr.x_weights_)
    # print('Y Weigths: \n%' % plsr.y_weights_)
    # print('X Scores: \n%' % plsr.x_scores_)
    # print('Y Scores: \n%' % plsr.y_scores_)

