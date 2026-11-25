"""
zones.py
Owner: Role 2 (Data & API)

Splits St. Gallen into named zones and counts e-scooters per zone.

Course concepts: classes with __init__, methods and __str__ (Unit 5,
Assignment 5), lists, dictionaries, the math module.
"""

import math


class Zone:
    """
    A zone is an area of the city around a centre point.
    Each zone has a name, a centre (latitude, longitude) and a radius in meters.
    """

    def __init__(self, zone_id, name, lat, lon, radius_m=600):
        self.zone_id = zone_id      # number used as a feature for the ML model
        self.name = name
        self.lat = lat
        self.lon = lon
        self.radius_m = radius_m

    def distance_to(self, lat, lon):
        """
        Distance in meters from the zone centre to a point.
        Simple approximation that is good enough inside one city:
        1 degree latitude ~ 111,000 m, 1 degree longitude ~ 75,000 m in St. Gallen.
        """
        dy = (lat - self.lat) * 111_000
        dx = (lon - self.lon) * 75_000
        return math.sqrt(dx * dx + dy * dy)

    def contains(self, lat, lon):
        """True if the point lies inside the zone's radius."""
        return self.distance_to(lat, lon) <= self.radius_m

    def __str__(self):
        return f'{self.name} ({self.lat:.4f}, {self.lon:.4f})'


# The coordinates are APPROXIMATE. Role 2: check them on a map and adjust.
ZONES = [
    Zone(0, 'HSG Campus', 47.4316, 9.3733),
    Zone(1, 'Hauptbahnhof', 47.4232, 9.3698),
    Zone(2, 'Altstadt / Marktplatz', 47.4262, 9.3770),
    Zone(3, 'Olma Messen', 47.4290, 9.3860),
]

# lookup tables: name -> Zone and id -> name
ZONES_BY_NAME = {zone.name: zone for zone in ZONES}
ZONE_NAMES_BY_ID = {zone.zone_id: zone.name for zone in ZONES}


def find_zone(lat, lon):
    """Returns the closest zone that contains the point, or None."""
    best_zone = None
    for zone in ZONES:
        if zone.contains(lat, lon):
            if best_zone is None or zone.distance_to(lat, lon) < best_zone.distance_to(lat, lon):
                best_zone = zone
    return best_zone


def count_per_zone(scooters):
    """
    scooters: list of (latitude, longitude) tuples
    returns:  dictionary {zone name: number of scooters}, every zone included
    """
    counts = {zone.name: 0 for zone in ZONES}
    for lat, lon in scooters:
        zone = find_zone(lat, lon)
        if zone is not None:
            counts[zone.name] += 1
    return counts
