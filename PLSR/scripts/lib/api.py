import os
import time

import hashlib
import requests


def md5_checksum(file_path):
    """
        Calculates the MD5 sum for a file (used for verification)
    """
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def get_client_id():
    try:
        return os.environ['CLIENT_ID']
    except KeyError:
        raise EnvironmentError('CLIENT ID has not been defined')


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


def upload_file(url, filename, metadata={}):
    """
        Sends a POST requests with a file to the API
    """
    while True:
        files = {'dataFile': open(filename, 'rb')}
        r = requests.post(url, files=files, data=metadata)

        # Check if everything went good
        if r.status_code is 200:
            res = r.json()

            if res['success'] and md5_checksum(filename) == res['md5']:
                print('[  OK  ] File uploaded successfully!')
                return True
            else:
                print('[  WARNING  ] Something went werong. Trying again...')
                time.sleep(10)
        else:
            print('[  ERROR  ] Connection error. Status code: {}'.format(r.status_code))