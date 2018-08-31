import os

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

plt.style.use('ggplot')

if __name__ == '__main__':
    common_file = '/disk/Data/data_simulation/all_in_one/output/common_data.csv'
    features_file = '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv'
    w_tilde_folder = '/disk/Data/data_simulation/center_1/output/admm'

    # Read X and Y and calculate W
    print('[  INFO  ] Reading CSV files...')
    X = pd.read_csv(common_file, index_col=0).values
    Y = pd.read_csv(features_file, index_col=0).values

    dx = X.shape[1]

    # Calculate W = (X'X)^(-1) * (X'Y)
    print('[  INFO  ] Calculating real W')
    # X_t_X_inv = np.linalg.solve(np.dot(X.T, X), np.eye(dx))
    # W = np.dot(X_t_X_inv, np.dot(X.T, Y))
    W_full_data = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, Y))

    errors = []
    for i in range(9):
        print('[  INFO  ] Calculating ')
        if i is 0:
            W_tilde = np.zeros_like(W_full_data)
        else:
            # Load W_tilde at iteration i
            w_tilde_file = os.path.join(w_tilde_folder, 'w_tilde_iter_%d.npz' % (i-1))
            W_tilde = np.load(w_tilde_file)['W_tilde']

        # print(W)
        print(
            'W_tilde itration %d\n\t- Mean: %f\n\t- Std: %f'
            % ((i - 1), W_tilde.mean(), W_tilde.std())
        )
        # Check mean squared error
        error = np.mean(np.abs((W_full_data - W_tilde) ** 2))
        errors.append(error)

    # Plot results
    print('Errors: {}'.format(errors))
    plt.figure(figsize=(19.2 * 0.5, 10.8 * 0.5), dpi=150)
    plt.plot(errors)
    plt.title('X %s | Y %s | rho (0.001)' % (str(X.shape), str(Y.shape)))
    plt.xlabel('Number of iterations')
    plt.ylabel('Mean square error')

    plt.figure()
    plt.scatter(Y[0], X.dot(W_tilde)[0], color='b')
    plt.title('Approximated data')
    plt.show()