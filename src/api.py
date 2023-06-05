"""Module interacting with library catalogue api"""


import json
import urllib.parse

import requests

from .env import (
    LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API,
    LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API,
    LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN,
    LIBRARY_CATALOGUE_SITE_API,
    LIBRARY_CATALOGUE_SITE_URL,
    MAX_NOTIFICATION_RESULTS_COUNT,
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


def get_library_catalogue_backoffice_urls():
    return [
        LIBRARY_CATALOGUE_BACKOFFICE_ITEMS_API,
        LIBRARY_CATALOGUE_BACKOFFICE_EITEMS_API,
    ]


def get_backoffice_latest_pids():
    created = get_last_week_date_range()
    published = get_last_five_years_range()
    query = get_full_query(created=created, pub_year=published, restricted=False)
    query_encoded = urllib.parse.quote(query)

    pids = []
    headers = {"Authorization": f"Bearer {LIBRARY_CATALOGUE_BACKOFFICE_API_TOKEN}"}
    for url in get_library_catalogue_backoffice_urls():
        response = requests.get(f"{url}{query_encoded}", headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"Request failed with status code: {e}")

        hits, _ = response.json().get("hits", {}).values()
        pids.extend(get_pids_from_docs(hits))

    return pids


def get_site_api_docs(query):
    query_encoded = urllib.parse.quote(query)

    response = requests.get(f"{LIBRARY_CATALOGUE_SITE_API}{query_encoded}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Request failed with status code: {e}")

    hits, count = response.json().get("hits", {}).values()
    if count == 0:
        return None
    # Send query link only if results > 20
    if count > int(MAX_NOTIFICATION_RESULTS_COUNT):
        return f"{LIBRARY_CATALOGUE_SITE_URL}{query_encoded}"

    return hits


def send_channel_request(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {NOTIFICATIONS_API_SECRET}",
    }
    request_data = {
        "target": NOTIFICATIONS_CHANNEL_ID,
        "summary": "Library Updates",
        "priority": "NORMAL",
        "body": data,
    }

    response = requests.post(
        NOTIFICATIONS_API_URL, headers=headers, data=json.dumps(request_data)
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Request failed with status code: {e}")

    return response.status_code
