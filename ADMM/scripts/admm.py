import os

import requests

import numpy as np

if __name__ == '__main__':
    server_url = 'http://localhost:3300/centers/admm'

    # Generate and save data
    test = 1e-4 * np.random.normal(1, 1, [200000, 20]).astype(np.float16)
    np.save('test.npy', test)

    files = {'sampleFile': open('test.npy', 'rb')}

    r = requests.post(server_url, files=files)

    print(r.text)

    if r.status_code is 200:
        r_json = r.json()
        if r_json['success']:
            print('Post successful!')
            uploaded_npy = np.load('/user/ssilvari/home/node/uploads/' + r_json['file'] + '.npy')

            print(np.mean((test - uploaded_npy) ** 2))
        else:
            print('API failed!')
    else:
        print('Error code', r.status_code)
