#!/usr/bin/env python3
__author__ = "Santiago Smith, Marco Lorenzi"
__copyright__ = "Copyright 2018, INRIA"
__description__ = """
This code performs a statistical centering
    python3 plsr_analysis.py -x [path_to_the_X_csv_file] -y [path_to_the_Y_csv_file]
"""

import os
import sys
import shutil
import logging
import argparse
import time, threading

import requests
import numpy as np
import pandas as pd

# Set root folder
root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root)

from lib.welford import Welford

# ========== FUNCTION DEFINITIONS ==========

def update_screen():
    os.system('cat ' + log_file)

def get_server_url():
    try:
        return os.environ['API_HOST'] + 'welford'
    except KeyError:
        return 'http://localhost/welford'

def get_client_id():
    try:
        return os.environ['CLIENT_ID']
    except KeyError:
        raise KeyError('Client ID has not been defined.')

def get_current_statistics():
    url = get_server_url()
    logger.debug('Connecting to server: {}'.format(url))

    # Pull data
    success = False
    while not success:
        r = requests.get(url)
        if r.status_code is 200:
            res = r.json()
            if res['success']:
                return res['data']
        else:
            logger.error('Connection error. Status code: {}'.format(r.satus_code))
        logger.info('Retrying in 10 seconds')
        time.sleep(10)

def upload_data(filename):
    while True:
        url = get_server_url() + '/data'

        metadata = {
            'id': get_client_id()
        }

        files = {'dataFile': open(filename, 'rb')}

        r = requests.post(url, data=metadata, files=files)
        status_code = r.status_code
        if status_code is 200:
            res = r.json()
            if res['success']:
                logger.info('Data uploaded successfully')
                if get_client_id() in get_current_statistics()['centers_done']:
                    return True
        else:
            logger.error('Connection error. Status code: {}'.format(status_code))
        
        logger.info('Retrying...')

def first_post(data):
    wf = Welford()

    # Calculate data
    wf(data)

    logger.info(
        '\n\t- Mean shape: {}\n\t- Variance shape{} \n\t- Observations: {}'
        .format(wf.M.shape, wf.S.shape, wf.k))
    
    # Save data
    statistics = {
        'k': wf.k,
        'mean': wf.M,
        'var': wf.S
    }

    stats_file = os.path.join(output_folder, 'welford_%s.npz' % get_client_id())
    np.savez_compressed(stats_file, **statistics)

    upload_data(stats_file)
    
def set_status(status: bool, id: str):
    url = get_server_url() + '/status/%s/%s' % (id, str(status))
    r = requests.put(url)
    if r.status_code is 200:
        logger.info('Server put in busy mode.')
    else:
        logger.error('Connection error - Status code: {}'.format(r.status_code))

def download_final_stats():
    success = False
    while not success:
        logger.info('Downloading current Welford data...')
        url = get_server_url() + '/data'
        dl_data_file = os.path.join(output_folder, 'welford_final.npz')
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(dl_data_file, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            logger.info('Data downloaded successfully')
            success = True
        else:
            logger.info('Error downloading welford data - Error code {}'.format(r.status_code))

def get_and_update(local_data):
    # Get current data
    success = False
    
    while not success:
        logger.info('Downloading current Welford data...')
        url = get_server_url() + '/data'
        dl_data_file = os.path.join(output_folder, 'welford_dl.npz')
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(dl_data_file, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            logger.info('Data downloaded successfully')
            success = True
        else:
            logger.info('Error downloading welford data - Error code {}'.format(r.status_code))

    # Update
    wf_old = np.load(dl_data_file)

    wf = Welford()
    wf.k = wf_old['k']
    wf.M = wf_old['mean']
    wf.S = wf_old['var']

    wf(local_data)

    logger.info(
        '\n\t- Mean shape: {}\n\t- Variance shape{} \n\t- Observations: {}'
        .format(wf.M.shape, wf.S.shape, wf.k))

    # Save data
    statistics = {
        'k': wf.k,
        'mean': wf.M,
        'var': wf.S
    }

    stats_file = os.path.join(output_folder, 'welford.npz')
    np.savez_compressed(stats_file, **statistics)

    # Upload new statistics
    upload_data(stats_file)


def main():
    # Get current status
    current_data = get_current_statistics()
    if current_data is None:
        logger.error('Looks like there are not pending tasks.')
        return True

    if not current_data['done'] and get_client_id() not in current_data['centers_done'] and not current_data['busy']:
        if get_client_id() not in current_data['centers']:
            logger.error('Center %s is not allowed to update. Please, contact support.' % get_client_id())
            return True

        # Get the main server busy
        set_status(True, current_data['_id'])
        
        logger.info('==== Starting Online statistics calculation ====')
        local_data = pd.read_csv(csv_file, index_col=0).values
        logger.info('Data info:\n\t- Data file: {}\n\t- Data shape: {}'.format(csv_file, local_data.shape))

        # 2. Update statistics
        if not current_data['centers_done']:
            logger.info('Looks like this is the first center posting data')
            first_post(local_data)
        else:
            logger.info('Updating statistics based on previous ones.')
            get_and_update(local_data)
        
        # Set the server free
        set_status(False, current_data['_id'])
    
    elif (not current_data['done'] and get_client_id() in current_data['centers_done']) or current_data['busy']:
        logger.info('Waiting for the others...')
        time.sleep(10)
    else:
        download_final_stats()
        return True


if __name__ == '__main__':
    csv_file = '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv'

    # Deal with the arguments
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('-data', metavar='data',
                        help='Path to the csv_file that contains the data to be centered',
                        default=csv_file)
    args = parser.parse_args()

    csv_file = args.data

    # LOGGING PARAMETERS
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    output_folder = os.path.join(os.path.dirname(csv_file), 'welford')
    
    if os.path.exists(output_folder):
        os.system('rm ' + output_folder + '/*')
    else:
        os.mkdir(output_folder)

    log_file = os.path.join(output_folder, 'welford.log')

    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Run data centering
    done = False
    while not done:
        # Refresh screen thread
        th = threading.Timer(1, update_screen)
        th.start()
        try:
            done = main()
            time.sleep(5)
        except requests.exceptions.ConnectionError as e:
            logger.exception(str(e))
        
        th._stop()
    print('DONE!')
    logger.info('DONE!')
