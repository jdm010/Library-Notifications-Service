"""Module interacting with library catalogue api"""


import json
import urllib.parse

import requests

from .env import (
    LIBRARY_CATALOGUE_BACKOFFICE_API,
    LIBRARY_CATALOGUE_SITE_API,
    NOTIFICATIONS_API_SECRET,
    NOTIFICATIONS_API_URL,
    NOTIFICATIONS_CHANNEL_ID,
)
from .utils import (
    get_full_query,
    get_last_five_years_range,
    get_last_week_date_range,
    get_pids_from_docs,
)


def get_backoffice_latest_pids():
    created = get_last_week_date_range()
    published = get_last_five_years_range()
    query = get_full_query(created=created, pub_year=published)

    query_encoded = urllib.parse.quote(query)
    response = requests.get(f"{LIBRARY_CATALOGUE_BACKOFFICE_API}{query_encoded}")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    hits, _ = response.json().get("hits", {}).values()
    pids = get_pids_from_docs(hits)

    return pids


def get_site_api_docs(query):
    query_encoded = urllib.parse.quote(query)

    response = requests.get(f"{LIBRARY_CATALOGUE_SITE_API}{query_encoded}")
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    hits, _ = response.json().get("hits", {}).values()
    return hits


def send_channel_request(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTIFICATIONS_API_SECRET}",
    }
    request_data = {
        "target": f"{NOTIFICATIONS_CHANNEL_ID}",
        "summary": "Library Updates",
        "priority": "NORMAL",
        "body": data,
    }

    response = requests.post(
        NOTIFICATIONS_API_URL, headers=headers, data=json.dumps(request_data)
    )

    return response.status_code
