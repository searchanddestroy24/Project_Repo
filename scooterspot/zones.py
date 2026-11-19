# zones.py
# Owner: Role 2 (Data & API)
#
# Splits St. Gallen into a few named zones and counts how many
# e-scooters are in each zone.
#
# Course concepts used: dictionaries, tuples, for loops, if/else,
# functions with default parameters, the math module.

import math

# Each zone has a name (key) and a centre point (value) as a tuple (latitude, longitude).
# The coordinates are APPROXIMATE. Check them on a map and adjust if needed.
ZONES = {
    'HSG Campus': (47.4316, 9.3733),
    'Hauptbahnhof': (47.4232, 9.3698),
    'Altstadt / Marktplatz': (47.4262, 9.3770),
    'Olma Messen': (47.4290, 9.3860),
}

# Scooters further away than this from every zone centre are counted as 'Other'.
MAX_DISTANCE_M = 600


def distance_in_meters(lat1, lon1, lat2, lon2):
    # Simple approximation that is good enough inside one city:
    # 1 degree latitude  is about 111,000 m
    # 1 degree longitude is about  75,000 m at the latitude of St. Gallen
    dy = (lat1 - lat2) * 111_000
    dx = (lon1 - lon2) * 75_000
    return math.sqrt(dx * dx + dy * dy)


def find_zone(lat, lon, max_distance=MAX_DISTANCE_M):
    # Returns the name of the closest zone, or 'Other' if no zone is close enough.
    best_zone = 'Other'
    best_distance = max_distance
    for zone_name, (zone_lat, zone_lon) in ZONES.items():
        distance = distance_in_meters(lat, lon, zone_lat, zone_lon)
        if distance < best_distance:
            best_distance = distance
            best_zone = zone_name
    return best_zone


def count_per_zone(scooters):
    # scooters is a list of (latitude, longitude) tuples.
    # Returns a dictionary like {'HSG Campus': 3, 'Hauptbahnhof': 7, ...}.

    # start every zone with 0, so that empty zones also show up in charts
    counts = {}
    for zone_name in ZONES:
        counts[zone_name] = 0
    counts['Other'] = 0

    # same counting pattern as roll_the_dice() in streamlit_demo.py
    for lat, lon in scooters:
        zone = find_zone(lat, lon)
        counts[zone] += 1
    return counts
