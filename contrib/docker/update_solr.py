#!/usr/bin/env python
import json
import requests
import time
from google.cloud import kms_v1

# decrypt api key
f = open("ckan_api_key.enc", "rb")
key = f.read()
client = kms_v1.KeyManagementServiceClient()
name = client.crypto_key_path_path('vwt-d-gew1-dat-solutions-cat', 'europe', 'ckan-api-key', 'ckan-api-key')
response = client.decrypt(name, key)
api_key = response.plaintext
api_key = api_key.strip()
# Use the json module to dump the dictionary to a string for posting.
url = 'https://ckan.test-app.vwtelecom.com/api/action/package_list'
# We'll use the package_create function to create a new dataset
headers = {
    'Content-Type': "application/json",
    'Authorization': api_key,
    'Host': "ckan.test-app.vwtelecom.com"
}
request = requests.post(url, headers=headers)
delete_url = 'https://ckan.test-app.vwtelecom.com/api/action/dataset_purge'
if request.status_code == 200:
    data = json.loads(request.text)
    print(data['result'])
    for i in data['result']:
        payload = {'id': i}
        delete_request = requests.post(delete_url, json=payload, headers=headers)
        print(delete_request.status_code)
        try:
            while delete_request.status_code == 500:
                delete_request = requests.post(delete_url, json=payload, headers=headers)
                print(delete_request.status_code)
                time.sleep(1)
            else:
                print('succeed')
        except delete_request:
            print("exception")
        else:
            if delete_request.status_code == 200:
                print("deleted")
            else:
                print(delete_request.status_code)
                print("not deleted")
else:
    print("Request failed")
    print(request.status_code)
    print(request.text)
