#!/usr/bin/env python
import json
import requests
import time
from google.cloud import kms_v1
from google.cloud import storage

print("start update_solr.pu")


def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print("blob {} downloaded to {}. " .format(source_blob_name, destination_file_name))


# decrypt api key
f = open("/workspace/ckan_api_key.enc", "rb")
print("api key open")
key = f.read()
print("api key read")
client = kms_v1.KeyManagementServiceClient()
print("api key client")
name = client.crypto_key_path_path('vwt-d-gew1-dat-solutions-cat', 'europe', 'ckan-api-key', 'ckan-api-key')
print("api key key path")
response = client.decrypt(name, key)
print("api key decrypted")
api_key = response.plaintext
print("api key plaintext")
api_key = api_key.strip()
print("api key stripped and ready")

# We'll use the package_create function to create a new dataset
headers = {
    'Content-Type': "application/json",
    'Authorization': api_key,
    'Host': "127.0.0.1:8080"
}

# Use the json module to dump the dictionary to a string for posting.
url = 'http://127.0.0.1:8080/api/action/package_list'
request = requests.post(url, headers=headers)
print("requested 1 time")
print(request.status_code)
delete_url = 'http://127.0.0.1:8080/api/action/dataset_purge'
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
    i = 0
    try:
        while request.status_code == 500 or request.status_code == 503:
            i = i+1
            request = requests.post(url, headers=headers)
            print(request.status_code)
            print("requested time "+i)
            time.sleep(5)
    except request.status_code:
        print("nothing")

# download from google cloud storage
download_blob("vwt-d-gew1-dat-solutions-cat-dcat-deployed-stg", "data_catalog.json", "/workspace/data_catalog.json")
file = open("/workspace/data_catalog.json", "r")
j = json.loads(file.read())
for data in j['dataset']:
    # Put the details of the dataset we're going to create into a dict.
    dataDict = {
        "name": data['identifier'],
        "title": data['title'],
        "notes": data['rights'],
        "owner_org": 'dat',
    }
    # name is used for url and cant have uppercase or spaces so we have to replace space with _ or - and upper to lower
    dataDict["name"] = dataDict["name"].replace("/", "_")
    dataDict["name"] = dataDict["name"].lower()
    # Use the json module to dump the dictionary to a string for posting.
    url = 'http://127.0.0.1:8080/api/action/package_create'
    # We'll use the package_create function to create a new dataset.
    request = requests.post(url, json=dataDict, headers=headers)
    try:
        while request.status_code == 500:
            request = requests.post(url, json=dataDict, headers=headers)
            print(request.status_code)
            time.sleep(1)
        else:
            print("success")
    except request:
        print("exception")
    if request.status_code == 200:
        print("success")
    else:
        print("Request failed")
        print(request.status_code)
        print(request.text)
    # create resource for dataset
    for resource in data['distribution']:
        description = resource.get('description')
        mediatype = resource.get('mediaType')

        resourceDict = {
            "package_id": dataDict["name"],
            "url": resource['accessURL'],
            "description": description,
            "name": resource['title'],
            "format": resource['format'],
            "mediaType": mediatype
        }
        resource_url = 'http://127.0.0.1:8080/api/action/resource_create'
        resource_request = requests.post(resource_url, json=resourceDict, headers=headers)
        if resource_request.status_code == 200:
            print("success!")
        else:
            print("Request failed")
            print(resource_request.status_code)
            print(resource_request.text)
