import os
import sys
import requests
from urlparse import urljoin

os.system('clear')

if __name__ == '__main__':
    api_url = sys.argv[1]
    n_centers = 4

    # Create centers
    centers = []
    for i in range(1, n_centers + 1):
        center = {
            'email': 'center_%d@center.fr' % i,
            'password': '1234',
            'info': 'This is center %d' % i,
            'enabled': True
        }
        centers.append(center)

    # 1. Register centers
    print('[  INFO  ] Registering centers and getting ids')
    for center in centers:
        url = urljoin(api_url, 'centers/new')
        r = requests.post(url, json=center)
        if r.status_code is 200:
            res = r.json()
            if res['success']:
                print(res)
    
    r = requests.get(urljoin(api_url, 'centers'))
    if r.status_code is 200:
        center_ids = list(r.json().keys())
        center_ids.remove('5ba1040e4a24c500103da1ba')
        center_ids = center_ids[:n_centers]
        print('\n[  INFO  ] Centers registered:', center_ids)
        for cid in center_ids:
            print(cid + '\n')
    
    # 2. Create a 'centering data (welford)' task
    r = requests.post(urljoin(api_url, 'welford/new'), json={'centers': center_ids})
    if r.status_code is 200:
        res = r.json()
        if res['success']:
            print('\n[  OK  ] %s' % res['msg'])

    # 3. Create an ADMM task
    admm_data = {
        'centers': center_ids,
        'rho': 0.001,
        'number_of_iterations': 10
    }

    r = requests.post(urljoin(api_url, 'admm'), json=admm_data)
    if r.status_code is 200:
        res = r.json()
        if res['success']:
            print('\n[  OK  ] %s | ID: %s' % (res['msg'], res['id']))
