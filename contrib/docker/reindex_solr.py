#!/usr/bin/env python
import requests
import sys
import json
import time

# decrypt api key
key = sys.argv[1]
# get hostname
host = sys.argv[2]
host = host.strip("https://")
project_id = sys.argv[3]
# We'll use the package_create function to create a new dataset
headers = {
    'Content-Type': "application/json",
    'Authorization': key,
    'Host': host
}
# remove all datasets from database
url = 'https://{}/api/action/package_list'.format(host)
request = requests.post(url, headers=headers)
delete_url = 'https://{}/api/action/dataset_purge'.format(host)
tries = 0
if request.status_code != 200:
    try:
        while request.status_code == 500 or request.status_code == 503 and tries < 15:
            request = requests.post(url, headers=headers)
            tries = tries + 1
            time.sleep(4)
    except request:
        print(request.status_code)
else:
    data = json.loads(request.text)
    for i in data['result']:
        payload = {'id': i}
        get_package_url = 'https://{}/api/action/package_show'.format(host)
        request_show = requests.post(get_package_url, json=payload, headers=headers)
        request_data = json.loads(request_show.text)
        request_data = request_data['result']
        update_url = 'https://{}/api/action/package_update'.format(host)
        update_request = requests.post(update_url, json=request_data, headers=headers)
        print(update_request.text)
        print(update_request.status_code)
