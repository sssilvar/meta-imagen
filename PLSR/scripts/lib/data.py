import os
import time
from datetime import datetime

import requests
import shutil
import hashlib
import numpy as np
import pandas as pd
import dateutil.parser
from .welford import Welford

log_filename = os.path.join(os.environ['DATA_FOLDER'], '.plsr')


def md5_checksum(file_path):
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def is_time_to_update(current_data, new_data):
    """
    Checks if there is data to be updated.
    :param current_data: The JSON object containing the current statistics (obtained from a HTTP request).
    :param new_data: The new JSON data to be updated
    :return: True or False
    """
    # Check last updated
    last_updated = dateutil.parser.parse(current_data['updated'])
    today = datetime.now()
    fmt = '%Y-%m-%dT%H:%M'

    # Reformat it up to minutes
    last_updated = last_updated.strftime(fmt)
    today = today.strftime(fmt)

    keys = ['currentAvgX', 'currentStdX', 'currentAvgY', 'currentStdY']

    conditions = []
    for key in keys:
        try:
            conditions.append(
                not np.array_equal(current_data[key], new_data[key])
            )
        except Exception as e:
            print(e)
    # Return the conditions:
    # If the date is newer and there is different data
    return today > last_updated and np.sum(conditions) > 0


def is_allowed_to_update():
    """Check if there is not existing operations from this client"""
    print('[  INFO  ] Checking if this client is allowed to update')

    if os.path.isfile(log_filename):
        df = pd.read_csv(log_filename, names=['id'])
    else:
        os.mknod(log_filename)
        df = pd.read_csv(log_filename, names=['id'])

    # Check if there is not previous transactions
    if df.shape[0] is 0:
        return True

    # Define server url and status
    server_url = get_server_url() + 'welford/info/'
    status = False

    for id in df['id']:
        print('[  INFO  ] Update with Id: ', id, ' found.')
        stat_url = server_url + id

        try:
            r = requests.get(stat_url)

            if r.status_code is 200:
                res = r.json()
                if res['success'] is True:
                    print('[  WARNING  ] This client has already uploaded data to the API server. '
                          'So, it is not allowed to post any results. Please contact support. Transaction ID: ', id)
                    print('[  INFO  ] No data has been uploaded')
                    return False
                else:
                    status = True
            else:
                print('[  ERRROR  ] Cannot connect to the API server. Error code: ', r.status_code)
                status = False
        except Exception as e:
            print('[  ERROR  ] Exception: ', str(e))
            return False

    return status


def cast_data(data):
    """
    Casts the data in order to be serializable as JSON.
    :param data: JSON data to be processed
    :return: A dict which can be serializable as JSON.
    """

    for key, val in data.items():
        if type(val) is np.ndarray and ('X' in key or 'Y' in key):
            data[key] = val.tolist()

    # Return processed data
    return data


def get_server_url():
    """
    Gets the API server URL (were the data is going to be shared). This works only if
    API_HOST variable is set.

    You can set this as:
        $ export API_HOST=[api_url]
    :return: str, API url
    """
    try:
        url = os.environ['API_HOST']
        # print('[  OK  ] Server url loaded: ', url)
    except KeyError:
        url = 'http://localhost:3300/'
        print('[  WARNING  ] API_HOST environment variable was not found. default server url was set at: ', url)

    return url


def post_data_to_api(json_data, server_url, mode='welford'):
    """
    Posts the data to the API server.
    :param json_data: JSON serializable dict containing all the data
    :param server_url: URL where data is being posted
    :return: bool - Successful or failed transmission
    """
    print('[  INFO  ] Posting at:' + server_url)
    # Create file
    data_file = 'data.npy'
    np.save(data_file, json_data)

    if mode is 'welford':
        metadata = {
            'iteration': json_data['currentK'],
            'updatedBy': get_client_id()
        }

        files = {'dataFile': open(data_file, 'rb')}

        # try 10 times
        counter = 10

        while counter > 0:
            # Send the POST request
            r = requests.post(server_url, files=files, data=metadata)

            # Check the operation
            if r.status_code is 200:
                res = r.json()
                if res['success'] is True:
                    print('\tData updated successfully')
                    with open(log_filename, 'a') as logfile:
                        logfile.write(res['id'] + '\n')

                    print('[  INFO  ] Update saved with id: ', res['id'])
                    print('[  OK  ] Transmission finished')
                    return True
                elif res['success'] is False:
                    print('[  ERROR  ] Transmission to server was not successful')
            elif r.status_code is not 200:
                print('[  ERROR  ] There is an HTTP error - Status bin: ', r.status_code)

            print('[  INFO  ] Trying to connect again')
            counter = counter - 1
            if counter is 0:
                print('[  ERROR  ] Number of tries exceeded')
                return False
            time.sleep(2)
        print('[  OK  ] Transmission finished')
        return False

    elif mode is 'center':
        metadata = {}

        files = {'dataFile': open(data_file, 'rb')}

        # try 10 times
        counter = 10

        while counter > 0:
            # Send the POST request
            r = requests.post(server_url, files=files, data=metadata)

            # Check the operation
            if r.status_code is 200:
                res = r.json()
                if res['success'] is True and res['md5'] == md5_checksum(data_file):
                    print('\tCenter data updated successfully')
                    print('[  OK  ] Transmission finished')
                    return True
                elif res['success'] is False:
                    print('[  ERROR  ] Transmission to server was not successful')
            elif r.status_code is not 200:
                print('[  ERROR  ] There is an HTTP error - Status bin: ', r.status_code)

            print('[  INFO  ] Trying to connect again')
            counter = counter - 1
            if counter is 0:
                print('[  ERROR  ] Number of tries exceeded')
                return False
            time.sleep(2)
        print('[  OK  ] Transmission finished')
        return False


def post_center_data(json_data, server_url):
    """
    Posts the data to the API server.
    :param json_data: JSON serializable dict containing all the data
    :param server_url: URL where data is being posted
    :return: bool - Successful or failed transmission
    """
    # Send the POST request
    r = requests.put(server_url, json=json_data)

    # Check the operation
    if r.status_code is 200:
        res = r.json()
        if res['success'] is True:
            print('\tData updated successfully')
            print('[  OK  ] Transmission finished')
            return True
        elif res['success'] is False:
            print('[  ERROR  ] Transmission to server was not successful')
    elif r.status_code is not 200:
        print('[  ERROR  ] There is an HTTP error - Status bin: ', r.status_code)

    print('[  OK  ] Transmission finished')


def recalculate_statistics(old_data, x_data, y_data):
    """
    Performs a Welford calculation for the mean and the variance vectors.
    :param old_data: JSON data obtained from the API
    :param x_data: Data obtained from the current PLSR analysis (X)
    :param y_data: Data obtained from the current PLSR analysis (Y)
    :return: None
    """
    # initialize a new data dictionary
    new_data = {
        'currentAvgX': [],
        'currentStdX': [],
        'currentAvgY': [],
        'currentStdY': [],
        'busy': False,
        'updatedBy': 'c6442cb6-b839-4d39-b874-15dca769e75d'  # TODO: this has to come from the key
    }

    # Check if old data exists
    if old_data is None:
        print('[  INFO  ] Looks like this is the first center in posting data!')
        for col in x_data.T:
            wfx = Welford()
            wfy = Welford()

            wfx(col)
            wfy(col)

            # Create the new data
            new_data['currentAvgX'].append(wfx.mean)
            new_data['currentStdX'].append(wfx.S)

            new_data['currentAvgY'].append(wfy.mean)
            new_data['currentStdY'].append(wfy.S)

            if wfx.k == wfy.k:
                new_data['currentK'] = wfx.k
            else:
                new_data['currentK'] = None
                print('[  ERROR  ] Number of observations for X and Y is not the same')
                return None

        # Return new data
        return new_data
    else:
        # Load the current data: mean, std and iteration
        for i in range(len(old_data['currentAvgX'])):
            "Start a for loop to recalculate the statistics element-wise (same length for all)"
            # Create a Welford object for X and Y
            wfx = Welford()
            wfy = Welford()

            # Initialize Welford method
            wfx.k = old_data['currentK']
            wfx.M = old_data['currentAvgX'][i]
            wfx.S = old_data['currentStdX'][i]

            wfy.k = old_data['currentK']
            wfy.M = old_data['currentAvgY'][i]
            wfy.S = old_data['currentStdY'][i]

            # For debugging
            # print('Current data: \n\tX: ', wfx, '\n\tY: ', wfy, '\n\tIteration: ', wfx.k, ' | ', wfy.k)

            # Recalculate statistics
            wfx(x_data[:, i])
            wfy(y_data[:, i])

            # For debugging
            # print('Current data: \n\tX: ', wfx, '\n\tY: ', wfy, '\n\tIteration: ', wfx.k, ' | ', wfy.k)

            # Create the new data
            new_data['currentAvgX'].append(wfx.mean)
            new_data['currentStdX'].append(wfx.S)

            new_data['currentAvgY'].append(wfy.mean)
            new_data['currentStdY'].append(wfy.S)

            if wfx.k == wfy.k:
                new_data['currentK'] = wfx.k
            else:
                new_data['currentK'] = 0
                print('[  ERROR  ] Number of observations for X and Y is not the same')
                return None

        # Return updated data
        return new_data


def center_exists(id, centers_url):
    "Checks if center id exists"
    r = requests.get(centers_url)

    if r.status_code is 200:
        res = r.json()
        if not res['success']:
            print('[  ERROR  ] Center ID was not found. Please, contact support.\n\tCenter id: ' + id)
            return False
        else:
            print('[  INFO  ] Center found in database. :)')
            return True


def get_number_of_observations(x, y):
    "Gets the number of observations and checks if X and Y are equal"
    nx = np.shape(x)[0]
    ny = np.shape(y)[0]
    if nx == ny:
        print('[  OK  ] Data consistent! :)\n\t Number of observations: ', nx)
        return nx
    else:
        raise ValueError('[  ERROR  ] X and Y observations are not the same! Check the data')


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
            return res['data']['statistics']
        else:
            print('[  ERROR  ] ', res['msg'])
    else:
        print('[  ERROR  ] ', r.text())


def get_api_data(data='statistics'):
    id = get_client_id()
    url = get_server_url()

    for i in range(10):
        if data is 'statistics':
            md5 = get_md5(url + 'centers/' + id)[-1]

            url = url + 'centers/statistics/' + id
            dl_data_file = 'statistics.npy'
        elif data is 'welford':
            # Get md5
            md5 = get_md5(url + 'welford/info')

            url = url + 'welford/data'
            dl_data_file = 'welford.npy'
        else:
            print('[  ERROR  ] Data request invalid')

        print('[  INFO  ] Getting ' + data + ' | MD5: ' + md5)

        # Send request to API
        print('[  INFO  ] Downloading ' + dl_data_file + ' from ' + url)
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(dl_data_file, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            if md5 == md5_checksum(dl_data_file):
                print('[  INFO  ] Download successful')
                return np.load(dl_data_file).item()
        print('[  INFO  ] Waiting 20 seconds for retrying')
        time.sleep(20)
    raise IOError('API is not responding - check internet connection or contact support')


def upload_stats_to_server(plsr):

    # Get X and Y matrices
    x_data = plsr.x
    y_data = plsr.y

    # Get client id
    center_id = get_client_id()

    # Define the url of the API
    stats_url = get_server_url() + 'welford'
    ul_stats_url = stats_url + '/data'
    center_url = get_server_url() + 'centers/' + center_id
    ul_center_url = get_server_url() + 'centers/statistics/' + center_id

    # Get the current statistics (API data is not being considered)
    avx, stx, avy, sty = plsr.GetStatistics()
    first_data = {
        'currentAvgX': avx,
        'currentStdX': stx,
        'currentAvgY': avy,
        'currentStdY': sty,
        'busy': False,
        'updatedBy': center_id
    }

    center_data = {
        "avX": np.array(avx).tolist(),
        "stX": np.array(stx).tolist(),
        "avY": np.array(avy).tolist(),
        "stY": np.array(sty).tolist(),
        "comp": np.array(plsr.ReturnComponents()).tolist(),
        "weights": np.array(plsr.GetWeights()).tolist(),
        "numberOfSubjects": get_number_of_observations(x_data, y_data)
    }

    # Check if center exists
    if center_exists(center_id, center_url):
        r = requests.get(stats_url + '/info')
        if r.status_code is 200:
            res = r.json()
            if res['success'] and res['data'] is not None:
                "Connection successful and data has been initialized"

                # Get data from JSON response
                api_data = get_api_data(data='welford')
                print('[  INFO  ] Last update id: ', res['data']['_id'])

                if is_allowed_to_update():
                    "Check if there is really new data to be updated"
                    # Recalculate statistics
                    new_data = recalculate_statistics(api_data, x_data, y_data)

                    # Post the results to the API
                    print('[  OK  ] Updating data into server: ' + stats_url)
                    post_data_to_api(new_data, ul_stats_url, mode='welford')
                    post_data_to_api(center_data, ul_center_url, mode='center')
            elif res['success'] and res['data'] is None:
                "Connection successful but, data has not been initialized (first time)"
                print('[  WARINING  ] Database has not been initialized. \n\tInitializing...')

                # Pre-process the data (serializable JSON)
                new_data = recalculate_statistics(old_data=None, x_data=x_data, y_data=y_data)

                # Post the data
                post_data_to_api(new_data, ul_stats_url, mode='welford')
                post_data_to_api(center_data, ul_center_url, mode='center')

        elif r.status_code is not 200:
            print('[  ERROR  ] Was not possible to connect to the server. '
                  'Check the server availability and/or the connection of your client.\n'
                  'Error code: {}'.format(r.status_code))
