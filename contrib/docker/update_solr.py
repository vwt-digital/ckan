#!/usr/bin/env python
import sys
import json
# import time
from google.cloud import storage
from ckanapi import RemoteCKAN, ValidationError
import logging


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
host_url = sys.argv[2]
host = RemoteCKAN(host_url, apikey=key)
project_id = sys.argv[3]

# download from google cloud storage
file_names = files_in_bucket("{}-dcats-deployed-stg".format(project_id))
for file in file_names:
    download_blob("{}-dcats-deployed-stg".format(project_id), file.name, "/tmp/data_catalog.json")  # nosec
    f = open("/tmp/data_catalog.json", "r")  # nosec
    j = json.loads(f.read())
    if('dataset' in j):
        for data in j['dataset']:
            # Put the details of the dataset we're going to create into a dict.
            # Using data.get sometimes because some values can remain empty while others should give an error
            dict_list = [
                {"access level": data.get('accessLevel')},
                {"Issued": data.get('issued')},
                {"Spatial": data.get('spatial')},
                {"Modified": data.get('modified')}
            ]
            maintainer = data.get('contactPoint').get('fn')
            data_dict = {
                "name": data['identifier'],
                "title": data['title'],
                "notes": data['rights'],
                "owner_org": 'dat',
                "maintainer": maintainer,
                "extras": dict_list
            }
            # name is used for url and cant have uppercase or spaces so we have to replace those
            data_dict["name"] = data_dict["name"].replace("/", "_")
            data_dict["name"] = data_dict["name"].replace(".", "-")
            data_dict["name"] = data_dict["name"].lower()
            resource_dict_list = []
            for resource in data['distribution']:
                description = resource.get('description')
                mediatype = resource.get('mediaType')
                resource_dict = {
                    "package_id": data_dict["name"],
                    "url": resource['accessURL'],
                    "description": description,
                    "name": resource['title'],
                    "format": resource['format'],
                    "mediaType": mediatype
                }
                resource_dict_list.append(resource_dict)
            try:
                # Put dataset on ckan
                host.action.package_create(name=data_dict["name"], owner_org=data_dict["owner_org"], data_dict=data_dict)
                # Put the resources on the dataset
                for resource_d in resource_dict_list:
                    host.action.resource_create(data_dict=resource_d)
            except ValidationError:
                # Except if dataset already exists
                print(f"Dataset {data_dict['name']} already exists, update")
                host.action.package_update(name=data_dict["name"], owner_org=data_dict["owner_org"], data_dict=data_dict)
                for resource_d in resource_dict_list:
                    # Try to add resource
                    try:
                        host.action.resource_create(package_id=resource_d["package_id"], data_dict=resource_d)
                    except ValidationError:
                        # Resource already exists
                        print(f"Resource {resource_d['name']} already exists, update")
                        host.action.resource_update(package_id=resource_d["package_id"], data_dict=resource_d)
            except Exception as e:
                logging.error(f'Exception occurred:{e}')
    else:
        print("JSON request does not contain a dataset")
