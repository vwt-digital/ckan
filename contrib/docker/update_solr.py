#!/usr/bin/env python
import json
import requests
import time
import sys
from google.cloud import storage


def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def files_in_bucket(bucket_name):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    return blobs


# decrypt api key
key = sys.argv[1]
print(key)
# get hostname
host = sys.argv[2]
print(host)
host = host.strip("https://")
print(host)
# We'll use the package_create function to create a new dataset
headers = {
    'Content-Type': "application/json",
    'Authorization': key,
    'Host': host
}

# Use the json module to dump the dictionary to a string for posting.
url = 'https://{}/api/action/package_list'.format(host)
request = requests.post(url, headers=headers)
delete_url = 'https://{}/api/action/dataset_purge'.format(host)
if request.status_code == 200:
    data = json.loads(request.text)
    for i in data['result']:
        payload = {'id': i}
        delete_request = requests.post(delete_url, json=payload, headers=headers)
        try:
            while delete_request.status_code == 500:
                delete_request = requests.post(delete_url, json=payload, headers=headers)
                time.sleep(1)
        except delete_request:
            print(delete_request.status_code)
else:
    try:
        while request.status_code == 500 or request.status_code == 503:
            request = requests.post(url, headers=headers)
            time.sleep(1)
    except request:
        print(request.status_code)
# download from google cloud storage
file_names = files_in_bucket("vwt-d-gew1-dat-solutions-cat-dcats")
for file in file_names:
    download_blob("vwt-d-gew1-dat-solutions-cat-dcats", file.name, "/workspace/data_catalog.json")
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
        # name is used for url and cant have uppercase or spaces so we have to replace those
        dataDict["name"] = dataDict["name"].replace("/", "_")
        dataDict["name"] = dataDict["name"].replace(".", "-")
        dataDict["name"] = dataDict["name"].lower()
        # Use the json module to dump the dictionary to a string for posting.
        url = 'https://{}/api/action/package_create'.format(host)
        # We'll use the package_create function to create a new dataset.
        request = requests.post(url, json=dataDict, headers=headers)
        try:
            while request.status_code == 500:
                request = requests.post(url, json=dataDict, headers=headers)
                time.sleep(1)
        except request:
            print(request.status_code)
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
            resource_url = 'https://{}/api/action/resource_create'.format(host)
            resource_request = requests.post(resource_url, json=resourceDict, headers=headers)
