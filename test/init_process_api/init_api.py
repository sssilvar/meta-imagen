import os
import requests

os.system('clear')

if __name__ == '__main__':
    api_url = 'http://ec2-34-217-66-229.us-west-2.compute.amazonaws.com:3300'
    n_centers = 8

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
        r = requests.post(api_url + '/centers/new', json=center)
        print(r.json())
        if r.status_code is 200:
            res = r.json()
            if res['success']:
                print(res)
    
    r = requests.get(api_url + '/centers')
    if r.status_code is 200:
        center_ids = r.json().keys()
        print('\n[  INFO  ] Centers registered:')
        for cid in center_ids:
            print(cid + '\n')
    
    # 2. Create a 'centering data (welford)' task
    r = requests.post(api_url + '/welford/new', json={'centers': center_ids})
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

    r = requests.post(api_url + '/admm/', json=admm_data)
    if r.status_code is 200:
        res = r.json()
        if res['success']:
            print('\n[  OK  ] %s | ID: %s' % (res['msg'], res['id']))
