import requests
import json


def getJsonOnline(url, headers):
    # making a GET request from url with headers and then loads the json
    return json.loads(requests.get(url, headers=headers).text)
