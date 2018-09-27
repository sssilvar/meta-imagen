#!/usr/bin/env python3
__author__ = "Santiago Smith, Marco Lorenzi"
__copyright__ = "Copyright 2018, INRIA"
__description__ = """
This program correlates structural features with common data in a decentralized way
by using ADMM as main method for optimising a Least Squares Linear regression.
Two files are necessary for this process:
    - groupfile_features.csv
    - common_data.csv

It is necessary to execute this code per each file as follows:

    python3 admm.py -c [path_to_the_common_data_csv] -f [path_to_the_features_file]
"""

__thanks__ = """


████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗    ██╗   ██╗ ██████╗ ██╗   ██╗██╗
╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║██║
   ██║   ███████║███████║██╔██╗ ██║█████╔╝      ╚████╔╝ ██║   ██║██║   ██║██║
   ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗       ╚██╔╝  ██║   ██║██║   ██║╚═╝
   ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗       ██║   ╚██████╔╝╚██████╔╝██╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚═╝
                                                                             
"""

import os
import time
import json
import shutil
import argparse
import logging

import requests
import hashlib

import numpy as np
from numpy import dot, eye
from numpy.linalg import solve

import pandas as pd

def md5_checksum(file_path):
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def get_server_url():
    """
    Gets the API server URL (were the data is going to be shared). This works only if
    API_HOST variable is set.

    You can set this as:
        $ export API_HOST=[api_url]
    :return: str, API url
    """
    try:
        url = os.environ['API_HOST'] + 'admm'
        # logger.info('Server url loaded: ', url)
    except KeyError:
        url = 'http://localhost:3300/admm/'
        logger.warning('API_HOST environment variable was not found. default server url was set at: {}'.format(url))

    return url

def get_client_id():
    try:
        return os.environ['CLIENT_ID']
    except KeyError:
        raise EnvironmentError('CLIENT ID has not been defined')

def get_md5(url):
    r = requests.get(url=url)

    if r.status_code is 200:
        res = r.json()
        if res['success']:
            return res['md5']
        else:
            logger.error(str(res['msg']))
    else:
        logger.error(str(r.status_code))

def gather_data_from_api(url, download=True):
    """
        Gathers data from API's url.
        Checks for ADMM id and current iteration.
    """
    # Emulation of a negative answer
    neg_res = {
        'id': None,
        'iteration': -1,
        'done': False,
        'busy': True,
        'rho': 0.01,
        'success': False
    }

    try:
        r = requests.get(url)

        if r.status_code is 200:
            res = r.json()
            if res['success'] and not res['busy']:
                cid, iteration, iter_done = res['id'], res['iteration'], res['admm']['iteration_finished']
                logger.info('ADMM process found with id: %s and iteration %d' % (cid, iteration))

                # Download data from master (admm)
                if iteration > 0 and download and iter_done:
                    dl_data_file = os.path.join(get_data_folder(), 'admm', 'w_tilde_iter_%d.npz' % (iteration - 1))
                    
                    data_url = get_server_url() + '/data/%d' % (iteration - 1)
                    r = requests.get(data_url, stream=True)

                    if r.status_code == 200:
                        logger.info('Gathering data from: %s and saving as: %s' % (data_url, dl_data_file))
                        with open(dl_data_file, 'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    
                return res
                # return {'id': cid, 'iteration': iteration, 'done': done, 'rho': rho, 'success': True}
            else:
                return neg_res
        else:
            logger.error('It was not possible to connect to the server. Try later or contact support.')
            return neg_res
    except Exception as e:
        logger.error('Exception occurred: %s' % str(e))
        return neg_res

def get_data_folder():
    """
        Gets current working directory
    """
    try:
        return os.environ['DATA_FOLDER']
    except KeyError:
        return os.path.dirname(args.f)

def get_current_status(api={'rho': 0.001}):
    current_status_file = os.path.join(get_data_folder(), 'admm', 'current.json')
    try:
        with open(current_status_file) as f:
            return json.load(f)
    except FileNotFoundError:            
        # Initialize current status
        current = {
            'iteration': 0,
            'rho': api['rho'],
            'done': False
        }

        # Save data
        with open(current_status_file, 'w') as fp:
            json.dump(current, fp, sort_keys=True, indent=4)
        return current

def update_current_status():
    logger.info('Updating status...')
    current_status_file = os.path.join(get_data_folder(), 'admm', 'current.json')

    current = get_current_status()
    current['iteration'] += 1

    # Save data
    with open(current_status_file, 'w') as fp:
        json.dump(current, fp, sort_keys=True, indent=4)

def upload_data(W_i, alpha_i, id):

    # Wait until master gets free
    api = gather_data_from_api(get_server_url(), download=False)
    logger.debug('Checking if Server is not busy at url {}.\n{}'.format(get_server_url(), api))
    while api['busy']:
        time.sleep(5)
        logger.info('Looks like another center is posting right now.')
        api = gather_data_from_api(get_server_url(), download=False)

    # Start Uploading data
    client_id = get_client_id()
    current = get_current_status()
    url = get_server_url() + '/upload/' + client_id
    admm_file = os.path.join(get_data_folder(), 'admm', 'admm_%s_iter_%d.npz' % (client_id, current['iteration']))
    logger.debug('URL: ' + url)

    # Save data
    if os.path.exists(admm_file):
        try:
            os.remove(admm_file)
        except OSError:
            logger.error('%s could not be deleted' % admm_file)

    np.savez_compressed(admm_file, **{'W_i': W_i, 'alpha_i': alpha_i, 'id': client_id})
    md5 = md5_checksum(admm_file)

    # Upload file
    # Create metadata
    metadata = {
        'id': client_id,
        'iteration': current['iteration']
        }

    files = {'dataFile': open(admm_file, 'rb')}

    # Send the POST request
    r = requests.post(url, files=files, data=metadata)

    # Check the operation
    if r.status_code is 200:
        res = r.json()
        msg = res['msg']
        logger.debug('Current status: {} | Response from API: {}'.format(current, msg))

        if res['success'] is True and md5 == res['md5']:
            logger.info('Data updated successfully')
            logger.info('Update saved in ADMM with id: {}'.format(res['id']))
            logger.info('Transmission finished')
            return 'successful'

        elif res['success'] is False:
            logger.error('Transmission to server was not successful:\n\t- Message: %s' % msg)
            if 'not allowed' in msg:
                return 'not allowed'

            elif 'already posted' in msg or 'busy' in msg or 'not update' in msg:
                print('Send request Failed!' + msg)
                return 'try again'

    elif r.status_code is not 200:
        logger.error('There is an HTTP error - Status bin: {}'.format(r.status_code))
        return 'http error'

def admm_update(X_i, Y_i, W_tilde, W_i, alpha_i, rho=0.001):
    """
        Performs the calculation of ADMM corresponding to
        the client (W_i and alpha_i)
    """
    # Get shapes
    dx = X_i.shape[1]

    # 1. Update W_i
    term_1 = solve(dot(X_i.T, X_i) + 0.5 * rho * eye(dx), eye(dx))  # Shape: (dx x dx)
    term_2 = dot(X_i.T, Y_i) - 0.5 * alpha_i + 0.5 * rho * W_tilde  # Shape: (dx x dy)
    W_i = dot(term_1, term_2)

    # 2. Update alpha_i
    alpha_i = alpha_i + rho * (W_i - W_tilde)

    return W_i, alpha_i

def download_last_w_tilde():
    while True:
        logger.info('Downloading last W_tilde update...')
        url = get_server_url()

        r = requests.get(url)
        if r.status_code is 200:
            res = r.json()

            if res['success'] and res['admm'] is not None:
                filename = os.path.join(get_data_folder(), 'admm', 'w_tilde_final.npz')

                data_url = get_server_url() + '/data/%d' % (res['admm']['number_of_iterations'] - 1)
                r = requests.get(data_url, stream=True)

                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    
                    return np.load(filename)['W_tilde']


def load_data(x_csv, y_csv, fillna=True):
    "Load CSV files as Dataframes (X and Y)"
    X = pd.read_csv(x_csv, index_col=0)
    Y = pd.read_csv(y_csv, index_col=0)

    if fillna:
        Y = Y.fillna(X.mean())
        X = X.fillna(X.mean())

    # TODO: REMOVE THIS
    Y['Age'] = Y['Age'].multiply(Y['Age'])  # Just correcting age^2
    
    return X, Y


def print_logger(log_file):
    os.system('tail ' + log_file)


def main():
    """
        Main ADDM function
        (Scheduled task so it starts working after the rest of the centers finish)
    """
    # =============== ADMM PROGRAM =============== 
    # 0.1 Gather data (if there is)
    logger.debug('Gathering data from API...')
    api = gather_data_from_api(get_server_url())
    logger.debug(str(api))

    # 0.2 Get current status:
    current = get_current_status(api)
    logger.debug('Current status: {}'.format(current))

    current_iter, api_iter = current['iteration'], api['iteration']

    if api['done']:
        logger.info('ADMM is done. Correcting data...')
        # Load features
        # Y: Feature data: args.f
        # X: common data: args.c
        X, Y = load_data(x_csv=args.c, y_csv=args.f, fillna=True)
        X = X.values

        # Load last iteration of W_tilde
        W_tilde = download_last_w_tilde()

        # Correct data
        Y_new = Y.values - X.dot(W_tilde)

        new_filename = os.path.join(get_data_folder(), os.path.basename(args.f).replace('centered.csv', 'admm.csv'))
        pd.DataFrame(Y_new, columns=Y.columns, index=Y.index).to_csv(new_filename)

        return True

    if current_iter == api_iter and api['success'] and not api['busy']:
        logger.info('Starting ADMM... (iteration %d)' % current_iter)
        # 1.1 Load X (Common data) and Y (Structural data)
        X, Y = load_data(x_csv=args.c, y_csv=args.f, fillna=True)

        # Deal with missing data    
        Y = Y.values
        X = X.values

        logger.info('Data dimensionality:\n\t- Features: %s\n\t- Common Data: %s' % (str(X.shape), str(Y.shape)))

        dx, dy = X.shape[1], Y.shape[1]
        rho = current['rho']

        # 1.2 Initialize alpha_i and W_i and W_tilde (if necessary)
        if current_iter == 0:
            W_tilde = np.zeros([dx, dy])
            W_i = np.zeros([dx, dy])
            alpha_i = np.zeros([dx, dy])
        else:
            dl_data_file = os.path.join(get_data_folder(), 'admm', 'w_tilde_iter_%d.npz' % (current['iteration'] - 1))
            admm_file = os.path.join(get_data_folder(), 'admm', 'admm_%s_iter_%d.npz' % (get_client_id(), current['iteration'] - 1))
            logger.debug('Loading W_tilde file: %s' % dl_data_file)
            logger.debug('Loading ADMM data file: %s' % dl_data_file)
            
            W_tilde = np.load(dl_data_file)['W_tilde']
            loc_data = np.load(admm_file)
            W_i = loc_data['W_i']
            alpha_i = loc_data['alpha_i']

            logger.info(
                'Alpha_i info:\n\t- Filename: %s\n\t- Mean: %f\n\t- Std: %f'
                % (admm_file, np.mean(alpha_i), np.std(alpha_i)))
            logger.info(
                'W_tilde info:\n\t- Filenames: %s\n\t- Mean: %f\n\t- Std: %f'
                % (dl_data_file, np.mean(W_tilde), np.std(W_tilde)))
        
        # 2. ADMM calculation
        W_i, alpha_i = admm_update(X, Y, W_tilde, W_i, alpha_i, rho=rho)
        logger.info('ADMM Output: \n\t- W_i shape: %s\n\t- alpha_i shape: %s' %(str(W_i.shape), str(alpha_i.shape)))

        # 3. Send data
        while True:
            status = upload_data(W_i, alpha_i, id=api['id'])
            api = gather_data_from_api(get_server_url(), download=False)

            if status is 'successful' and get_client_id() in api['admm']['centers_done']:
                # Update current status
                update_current_status()
                # 4. Wait for next iteration or finish iterating
                return False
            elif status is 'not allowed':
                return True
            else:
                logger.info('Something went wrong. Trying again...')
                print_logger(log_file)
                time.sleep(20)

    elif current['iteration'] == api['iteration'] + 1:
        print('[  INFO ] Still waiting for master to recalculate...')
        return False
    elif current['iteration'] < api['iteration']:
        print('[  ERROR ] Master iteration larger than center iteration. Does not make sense.')
        return True

if __name__ == '__main__':    
    # Parse the parameters (defining default values)
    feats_def = '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv'
    common_def = '/disk/Data/data_simulation/all_in_one/output/common_data.csv'

    # Deal with the arguments
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-c', metavar='common_csv',
                        help='Path to the csv file that contains the common data (age, educational level, etc.)',
                        default=common_def)
    parser.add_argument('-f', metavar='features_csv',
                        help='Path to the csv file that contains the structural features.',
                        default=feats_def)
    args = parser.parse_args()

    try:
        os.mkdir(os.path.join(get_data_folder(), 'admm'))
    except FileExistsError:
        print('[  WARNING  ] ADMM folder already exists')
    
    # Clear everything
    cmd = 'rm ' + os.path.join(get_data_folder(), 'admm') + '/*'
    os.system(cmd)

    # ======= SetUp and start logger =======
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    log_file = os.path.join(get_data_folder(), 'admm', 'admm_center.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # ======= START ADMM (CLIENT) =======
    done = False
    try:
        while not done:
            done = main()
            if not done:
                print_logger(log_file)
                logger.info('Waiting for API to update...')
                time.sleep(np.random.randint(10, 50))
    except Exception as e:
        print_logger('ERROR: %s - %s' % ( str(type(e)), str(e) ))
        raise SystemExit
    
    print(__thanks__)
    print('DONE!')
    logger.info('DONE!')