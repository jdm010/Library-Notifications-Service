"""Module interacting with library catalouge api"""


import requests
import urllib.parse

from .env import LIBRARY_CATALOUGE_SERVER, LIBRARY_CATALOUGE_SERVER_SUFFIX


def make_api_request(query):
    library_url = LIBRARY_CATALOUGE_SERVER + LIBRARY_CATALOUGE_SERVER_SUFFIX
    query_encoded = urllib.parse.quote(query)

    response = requests.get(f"{library_url}{query_encoded}")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
    
    hits, total = response.json().get("hits", {}).values()
    return hits, total
