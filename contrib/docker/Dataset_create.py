#!/usr/bin/env python
import json
import requests
from google.cloud import kms_v1
# decrypt api key
f = open("ckan_api_key.enc", "rb")
key = f.read()
client = kms_v1.KeyManagementServiceClient()
name = client.crypto_key_path_path('vwt-d-gew1-dat-solutions-cat', 'europe', 'ckan-api-key', 'ckan-api-key')
response = client.decrypt(name, key)
api_key = response.plaintext
api_key = api_key.strip()


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


urlid = is_downloadable("https://00e9e64bac60bf971d3c559af13006b129d348a93370cccb97-apidata.googleusercontent.com/download/storage/v1/b/vwt-d-gew1-dat-solutions-cat-dcat-deployed-stg/o/data_catalog.json?qk=AD5uMEsi_pHxezA24SijZDeOQnq-_pgIJyfED_098RsVJeD_M05WFCboGiu9wjo9DRU3MmeQcpTrlUBgsY-jRq-mrIyhxaHA4sEEnr8EDfwlZH2GGv9-OYFneMtzNhv9HZkCFG80Or6cq-LaVZOUFWkyyWfVnEjZSfXPuZpxVQnQd0V68A9Os6JtDfoHj8xg81J2Zjfzm93-lrCM9_HZIOYC9AFIljNUua--khiuQ8KFvxzSeOQ0EDiv4etpXfgCYBdBnUqrKq2TxYYh1rG6c-fenZYsbq5HF5yPNZ3FXXjMASzEUhAIlEYZt9wF31BC3erRouzL7kHrK3i4401hKatMT45--Ty_Ik9g9La0es5C7wQspMddqsckq7j85n5LUYPGzSu_PeQ0oNeCMNpcaKacYem-zsMWlLYuAIeHJi5Lbvodp7_ZE8gqOYHTFJr8ZTOvQSAymC7EUa4_wiAR9VBYewfC0lIXGBBDovi9GH5GkIND7p6BzF4M2T5kFjwfiLOTbClxJgh508lq96MEAfUo_7DW1V_v7o3ze1IsLZWJU4L8g2hvxOK-tsKLshzB1xb5xzNex7zksrZ6MFE0x1-u5j-0mcNqfrLVZfdHbr2sdRqcUwp_7Wl1mFG6QUwKy-WMHCICA9jS7m4ITcdiNnELO5fE2IlEXhL_gQy-1yWGJ0QG_-GebhPoDVCC32s5JylNKqIvz5NuzDowMqH1eBn8eJ4tuCZMM-QhSjg2VhLlRlOkQSmsC-hJQwPgJ9B0FUB52qhyMasXRi5jkQdlOKjrvCvtSa3fWnTyaM6i-Tjp0KxqGI78IwXPZgsTclwVwAsgFfgvJ_y0YiPFfyihZ_LNk_uOtk1F-Q")
print(urlid)
response = requests.get("https://00e9e64bac60bf971d3c559af13006b129d348a93370cccb97-apidata.googleusercontent.com/download/storage/v1/b/vwt-d-gew1-dat-solutions-cat-dcat-deployed-stg/o/data_catalog.json?qk=AD5uMEsi_pHxezA24SijZDeOQnq-_pgIJyfED_098RsVJeD_M05WFCboGiu9wjo9DRU3MmeQcpTrlUBgsY-jRq-mrIyhxaHA4sEEnr8EDfwlZH2GGv9-OYFneMtzNhv9HZkCFG80Or6cq-LaVZOUFWkyyWfVnEjZSfXPuZpxVQnQd0V68A9Os6JtDfoHj8xg81J2Zjfzm93-lrCM9_HZIOYC9AFIljNUua--khiuQ8KFvxzSeOQ0EDiv4etpXfgCYBdBnUqrKq2TxYYh1rG6c-fenZYsbq5HF5yPNZ3FXXjMASzEUhAIlEYZt9wF31BC3erRouzL7kHrK3i4401hKatMT45--Ty_Ik9g9La0es5C7wQspMddqsckq7j85n5LUYPGzSu_PeQ0oNeCMNpcaKacYem-zsMWlLYuAIeHJi5Lbvodp7_ZE8gqOYHTFJr8ZTOvQSAymC7EUa4_wiAR9VBYewfC0lIXGBBDovi9GH5GkIND7p6BzF4M2T5kFjwfiLOTbClxJgh508lq96MEAfUo_7DW1V_v7o3ze1IsLZWJU4L8g2hvxOK-tsKLshzB1xb5xzNex7zksrZ6MFE0x1-u5j-0mcNqfrLVZfdHbr2sdRqcUwp_7Wl1mFG6QUwKy-WMHCICA9jS7m4ITcdiNnELO5fE2IlEXhL_gQy-1yWGJ0QG_-GebhPoDVCC32s5JylNKqIvz5NuzDowMqH1eBn8eJ4tuCZMM-QhSjg2VhLlRlOkQSmsC-hJQwPgJ9B0FUB52qhyMasXRi5jkQdlOKjrvCvtSa3fWnTyaM6i-Tjp0KxqGI78IwXPZgsTclwVwAsgFfgvJ_y0YiPFfyihZ_LNk_uOtk1F-Q")
j = json.loads(response.text)
for data in j['dataset']:
    # Put the details of the dataset we're going to create into a dict.
    tags = data.get('keywords')
    dataDict = {
        "name": data['identifier'],
        "title": data['title'],
        "notes": data['rights'],
        "owner_org": 'dat'
    }
    # name is used for url and cant have uppercase or spaces so we have to replace space with _ or - and upper to lower
    dataDict["name"] = dataDict["name"].replace("/", "_")
    dataDict["name"] = dataDict["name"].lower()
    # Use the json module to dump the dictionary to a string for posting.
    url = 'https://ckan.test-app.vwtelecom.com/api/action/package_create'
    # We'll use the package_create function to create a new dataset.
    headers = {
        'Content-Type': "application/json",
        'Authorization': api_key,
        'Host': "ckan.test-app.vwtelecom.com"
    }
    request = requests.post(url, json=dataDict, headers=headers)
    if request.status_code == 200:
        print("succes")
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
        resource_url = 'https://ckan.test-app.vwtelecom.com/api/action/resource_create'
        resource_request = requests.post(resource_url, json=resourceDict, headers=headers)
        if resource_request.status_code == 200:
            print("succes!")
        else:
            print("Request failed")
            print(resource_request.status_code)
            print(resource_request.text)
