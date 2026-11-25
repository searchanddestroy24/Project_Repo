"""
make_sample_data.py
Owner: Role 3 (Machine Learning)

Creates FAKE observations in data/sample.db so that the whole app, including
the ML model, can be developed before enough real data has been collected.

    !!! These numbers are random. They must NOT appear in the final app or video. !!!

Run once:   python make_sample_data.py

Course concepts: random.randrange (Unit 2/4 roll-the-dice demo), loops, sqlite3.
"""

import random

import database
import zones


def fake_count(zone_id, hour):
    """A little realism: more scooters in the daytime, most at the station."""
    if 7 <= hour <= 19:
        base = 4
    else:
        base = 1
    if zones.ZONE_NAMES_BY_ID[zone_id] == 'Hauptbahnhof':
        base += 2
    return max(0, base + random.randrange(-3, 4))


def make_sample_data(days=14, every_minutes=30):
    DB = database.connect(database.SAMPLE_DB)
    with DB:
        DB.execute('DELETE FROM observations')   # start from an empty table
    rows = 0
    for day in range(days):
        weekday = day % 7
        for hour in range(24):
            for minute in range(0, 60, every_minutes):
                timestamp = f'SAMPLE-day{day + 1:02d} {hour:02d}:{minute:02d}'
                counts = {zone.zone_id: fake_count(zone.zone_id, hour) for zone in zones.ZONES}
                database.save_counts(DB, timestamp, weekday, hour, counts)
                rows += len(counts)
    DB.close()
    print(f'wrote {rows} FAKE rows to {database.SAMPLE_DB}')


make_sample_data()
