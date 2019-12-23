#!/usr/bin/env python
import json
import requests

# Use the json module to dump the dictionary to a string for posting.
url = 'https://ckan.test-app.vwtelecom.com/api/action/package_list'
# We'll use the package_create function to create a new dataset.
decrypted = open("/workspace/ckan_api_key.txt")
api_key = decrypted.read()
print(api_key)
headers = {
    'Content-Type': "application/json",
    'Authorization': api_key,
    'Host': "ckan.test-app.vwtelecom.com"
}
request = requests.post(url, headers=headers)
delete_url = 'https://ckan.test-app.vwtelecom.com/api/action/dataset_purge'
if request.status_code == 200:
    print("succes")
    data = json.loads(request.text)
    print(data['result'])
    for i in data['result']:
        payload = {'id': i}
        delete_request = requests.post(delete_url, json=payload, headers=headers)
        if delete_request.status_code == 200:
            print("deleted")
        else:
            print(delete_request.status_code)
            print("not deleted")
else:
    print("Request failed")
    print(request.status_code)
    print(request.text)
