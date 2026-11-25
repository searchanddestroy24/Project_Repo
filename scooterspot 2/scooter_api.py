"""
scooter_api.py
Owner: Role 2 (Data & API)

Loads the current positions of all available e-scooters around St. Gallen
from the sharedmobility.ch REST API of the Swiss Federal Office of Energy (BFE).
Data licence: free use, source must be credited ("Source: BFE, sharedmobility.ch").
API documentation (EXTERNAL): https://github.com/SFOE/sharedmobility

Course concepts: requests.get, status_code check and response.json()
(Unit 6 demo poke-api-client.py, Assignment 6), request parameters as a
dictionary (Assignment 6 hints), lists and tuples.
"""

import requests

API_URL = 'https://api.sharedmobility.ch/v1/sharedmobility/identify'

# centre of St. Gallen and search radius
CENTER_LAT = 47.4245
CENTER_LON = 9.3767
RADIUS_M = 2500


def fetch_page(offset):
    """Asks the API for one page of e-scooters. Returns the parsed JSON."""
    params = {
        'filters': 'ch.bfe.sharedmobility.vehicle_type=E-Scooter',
        'Geometry': f'{CENTER_LON},{CENTER_LAT}',   # the API wants longitude first
        'Tolerance': RADIUS_M,
        'offset': offset,
        'geometryFormat': 'esrijson',
    }
    response = requests.get(API_URL, params=params, timeout=10)

    # same pattern as poke-api-client.py from the lecture
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f'API request failed with status code {response.status_code}')


def fetch_scooters(max_pages=20):
    """
    Returns a list of (latitude, longitude) tuples, one per available e-scooter.

    The API returns its results in pages, so we keep asking with a growing
    offset until a page comes back empty.

    TODO Role 2: run `python check_setup.py` and check that the keys
    'geometry', 'x' and 'y' match the raw output. Adjust the lines below if not.
    """
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
