#!/usr/bin/env python
import requests
import sys
import json
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

# download from google cloud storage
file_names = files_in_bucket("{}-dcats".format(project_id))
for file in file_names:
    download_blob("{}-dcats".format(project_id), file.name, "/tmp/data_catalog.json")
    f = open("/tmp/data_catalog.json", "r")
    j = json.loads(f.read())
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
        if request.status_code == 200:
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
        elif request.status_code == 409:
            # if dataset exist we want to update it
            print(request.text)
            update_url = 'https://{}/api/action/package_update'.format(host)
            update_request = requests.post(update_url, json=dataDict, headers=headers)
            if update_request.status_code == 200:
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
                    resource_url = 'https://{}/api/action/resource_update'.format(host)
                    resource_request = requests.post(resource_url, json=resourceDict, headers=headers)
