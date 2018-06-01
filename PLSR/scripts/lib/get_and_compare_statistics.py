import numpy as np
import requests
import matplotlib.pyplot as plt


def get_data(surl):
    r = requests.get(surl)

    if r.status_code is 200:
        res = r.json()
        try:
            if res['success']:
                return res['msg']
            else:
                print('[  ERROR ] Data not found.')
                return None
        except KeyError:
            return res
    else:
        print('[  ERROR  ] Connection and/or request error. - Code ', r.status_code)
        return None


if __name__ == '__main__':
    # Set servers name
    global_data_surl = 'http://localhost:3300/centers/5b100d89b0395f0011263592'
    iterative_data_surl = 'http://ec2-34-217-80-61.us-west-2.compute.amazonaws.com:3300/stats'

    # Get data from servers
    global_data = get_data(global_data_surl)
    iterative_data = get_data(iterative_data_surl)

    print(global_data.keys())

    # Get number of subjects from the iterative data: N
    N = iterative_data['currentK']

    # Get data calculated from multiple centers
    avx_it = np.array(iterative_data['currentAvgX'])
    stx_it = np.sqrt(np.array(iterative_data['currentStdX']) / (N - 1))
    avy_it = np.array(iterative_data['currentAvgY'])
    sty_it = np.sqrt(np.array(iterative_data['currentStdY']) / (N - 1))

    # Get global data
    avx_g = np.array(global_data['avX'])
    stx_g = np.array(global_data['stX'])
    avy_g = np.array(global_data['avY'])
    sty_g = np.array(global_data['stY'])

    # Calculate absolute errors
    avx_err = abs(avx_g - avx_it) / avx_g
    stx_err = abs(stx_g - stx_it) / stx_g
    avy_err = abs(avy_g - avy_it) / avy_g
    sty_err = abs(sty_g - sty_it) /sty_g

    # plot the results
    plt.figure()
    plt.style.use('ggplot')

    plt.subplot(2, 2, 1)
    plt.title('Avg. X %err')
    plt.plot(avx_err)

    plt.subplot(2, 2, 2)
    plt.title('Avg. Y %err')
    plt.plot(avy_err)

    plt.subplot(2, 2, 3)
    plt.title('Std. X %err')
    plt.plot(stx_err, color='b')

    plt.subplot(2, 2, 4)
    plt.title('Std. Y %err')
    plt.plot(sty_err, color='b')

    plt.show()

