# scooter_api.py
# Owner: Role 2 (Data & API)
#
# Loads the current positions of all e-scooters around St. Gallen from the
# sharedmobility.ch API of the Swiss Federal Office of Energy (BFE/SFOE).
# Data: free use, source must be credited ("Source: BFE, sharedmobility.ch").
#
# Course concepts used: requests.get with timeout and raise_for_status
# (Unit 4 bonus notebook), f-strings, lists, tuples, for loops, functions.
#
# Lines marked "NOT FROM COURSE MATERIAL" use something that is not in the
# lecture/exercise files so far. They are kept as short as possible.

import requests

API_URL = 'https://api.sharedmobility.ch/v1/sharedmobility/identify'

# Centre of St. Gallen (longitude, latitude) and search radius in meters
CENTER_LON = 9.3767
CENTER_LAT = 47.4245
RADIUS_M = 2500


def fetch_page(offset, lon=CENTER_LON, lat=CENTER_LAT, radius=RADIUS_M):
    # Asks the API for one "page" of e-scooters within radius meters of (lat, lon).
    # %3D is "=" and %2C is "," written in URL form.
    url = (f'{API_URL}?filters=ch.bfe.sharedmobility.vehicle_type%3DE-Scooter'
           f'&Geometry={lon}%2C{lat}&Tolerance={radius}'
           f'&offset={offset}&geometryFormat=esrijson')
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()  # NOT FROM COURSE MATERIAL: turns the JSON text into Python lists/dicts


def fetch_scooters(max_pages=20):
    # Returns a list of (latitude, longitude) tuples, one per available e-scooter.
    #
    # The API returns results in pages, so we keep asking with a growing
    # offset until a page comes back empty (or we reach max_pages).
    #
    # TODO Role 2: run print(fetch_page(0)[:2]) once and check that the keys
    # 'geometry', 'x' and 'y' are correct. Adjust the lines below if not.
    scooters = []
    offset = 0
    for page in range(max_pages):
        items = fetch_page(offset)
        if len(items) == 0:
            break
        for item in items:
            geometry = item['geometry']
            # in esrijson, x is the longitude and y is the latitude
            scooters.append((geometry['y'], geometry['x']))
        offset += len(items)
    return scooters
