"""
database.py
Owner: Role 2 (Data & API)

Stores our collected observations in a SQLite database and reads them back.
One row = how many e-scooters were in one zone at one point in time.

Table `observations`:
    id          INTEGER, PRIMARY KEY (created automatically)
    timestamp   TEXT,    e.g. '2026-11-19 10:30'
    weekday     INTEGER, 0 = Monday ... 6 = Sunday
    hour        INTEGER, 0 ... 23
    zone_id     INTEGER, see zones.py
    count       INTEGER, number of e-scooters in the zone

Course concepts: sqlite3.connect, CREATE TABLE / INSERT INTO (Unit 7 bonus
notebook), "with DB: DB.execute(...)" for writing and "?" placeholders for
parameters (Assignment 7, Task 2 and 5), pd.read_sql for reading (Unit 7,
streamlit_db_demo.py).
"""

import sqlite3

import pandas as pd

REAL_DB = 'data/scooters.db'       # real data, written by collector.py
SAMPLE_DB = 'data/sample.db'       # FAKE data for development, made by make_sample_data.py


def connect(db_file=REAL_DB):
    """Opens the database and makes sure the table exists."""
    DB = sqlite3.connect(db_file)
    with DB:
        DB.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id        INTEGER PRIMARY KEY,
                timestamp TEXT    NOT NULL,
                weekday   INTEGER NOT NULL,
                hour      INTEGER NOT NULL,
                zone_id   INTEGER NOT NULL,
                count     INTEGER NOT NULL
            )
            """)
    return DB


def save_counts(DB, timestamp, weekday, hour, counts_by_zone_id):
    """
    Writes one row per zone.
    counts_by_zone_id: dictionary {zone_id: count}
    """
    with DB:
        for zone_id, count in counts_by_zone_id.items():
            # "?" placeholders instead of f-strings protect against SQL injection
            DB.execute(
                'INSERT INTO observations (timestamp, weekday, hour, zone_id, count) VALUES (?, ?, ?, ?, ?)',
                (timestamp, weekday, hour, zone_id, count),
            )


def load_observations(db_file=REAL_DB):
    """Returns all observations as a pandas DataFrame (empty if there are none)."""
    DB = connect(db_file)
    df = pd.read_sql('SELECT * FROM observations ORDER BY timestamp', DB, index_col=['id'])
    DB.close()
    return df
