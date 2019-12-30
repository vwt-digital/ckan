#!/usr/bin/env python
import json
import requests
from google.cloud import kms_v1
# decrypt api key
f = open("/workspace/ckan_api_key.enc", "rb")
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
response = requests.get("https://00e9e64bac87e9383534786d267b03f592a0a59642b0d6ae75-apidata.googleusercontent.com/download/storage/v1/b/vwt-d-gew1-dat-solutions-cat-dcat-deployed-stg/o/data_catalog.json?qk=AD5uMEsywKUK9AHqC0Zo_ooZkqm_rKOH0-RDtuhogUNZKGhyTnT2cw_Bczp1oFrQDfUalbbVJaWfPvkoAeBTSTGBCNAxrMmSlUWRK4JQ7M1ajI8PBt20XHcEPGUNsK9TOjJCBQQoCmYLco7AhUxw5a2ewzEj1ZMQDgXhVSYYuhuhkWct3O0PDqabEnubedWVnneszD2bLF-OG-NlG27sBwoCwu24h_02pVZLqjPRxXor21XlcuUoysjuoxXd68J0uMy6ZCUGVwW62CdV1UYCd4RgYIUyla9QRaNqwgcG7Y589ZxnVAd6cVWxcfKoNN45OtBqVPeAspENaYYTLireRvLBfqQYbDdtgi8UbAA3E91v7WN6plq-vsVSEqslXHVQ5ZCMEO1B9Eh4WZFDK-mOEKEzbo12B_rpazmZWD2kL0UEAh79IM4prWOdD_wKMbS2x1ws8ZeszFVylI9oALh7I7Llg33EvsLf_q2CR4YV-Kv0xSL1gd76ZO3yf9Qdu06tDJTzJJJzKhoq24pdn35amqQd8C_RlPgCs-yngaU2jSWZhAWMvB5q6RgAkUCCNXwItp5TwoIeFa2FG0wZsxQvhp9H8E98xw_FdF004BOBOYR7d44BsYMNboGwAPECd5mQzAHr8rHfq_vCWTsGRDvfagV9k_O1M0bW9gj0nslNhyc8xhbKwoOQaCfIbKVgERhB_59nuLQvjMPyvYQpvYb6Z6YQkGvlG1QwTgSfKPYAfWqUPbzXH1mo0i3Qq4C1E28IRsX6y4A5huTgFKig8Y5QGZDAmSgT97HoP3Qp3KsSsQcQaf3gIOx7baa2RS8C5IDdpiv7Rs25DVmP7WWptSlb-tLUaPRdIuA4Mg")
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
