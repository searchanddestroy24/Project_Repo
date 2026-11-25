"""
collector.py
Owner: Role 2 (Data & API)

Builds our own dataset for the machine learning model. The API only shows the
scooters available RIGHT NOW, so we ask it regularly and save the counts per
zone into the SQLite database data/scooters.db.

Run it from the project folder:   python collector.py
Keep it running as long as possible (the laptop must stay awake).
Push data/scooters.db to GitHub every few days (only Role 2 commits this file,
otherwise you get merge conflicts on a binary file).

Course concepts: datetime.now() and strftime (Assignments 5 and 6),
the time module (Assignment 6), functions, while loops.
"""

import time
from datetime import datetime

import database
import scooter_api
import zones

EVERY_MINUTES = 30


def collect_once(DB):
    scooters = scooter_api.fetch_scooters()
    counts = zones.count_per_zone(scooters)

    # convert {zone name: count} into {zone id: count} for the database
    counts_by_zone_id = {zones.ZONES_BY_NAME[name].zone_id: count for name, count in counts.items()}

    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M')
    database.save_counts(DB, timestamp, now.weekday(), now.hour, counts_by_zone_id)
    print(f'{timestamp}: saved {len(scooters)} scooters {counts}')


def run():
    DB = database.connect()
    while True:
        collect_once(DB)
        # EXTERNAL: time.sleep() pauses the program (Python docs, module "time")
        time.sleep(EVERY_MINUTES * 60)


run()
