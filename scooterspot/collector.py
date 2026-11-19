# collector.py
# Owner: Role 2 (Data & API)
#
# Builds our own dataset for the machine learning model.
# The API only shows the scooters available RIGHT NOW, so we ask it
# regularly and append the counts per zone to data/history.csv.
#
# Run it from the project folder with:   python collector.py
# Keep it running as long as possible (the laptop must stay awake).
# The more rows we collect, the better the predictions.
#
# One line in data/history.csv looks like this:
#   2026-11-19 10:30,3,10,HSG Campus,4
#   (time, weekday 0=Monday ... 6=Sunday, hour, zone, number of scooters)

import time                    # NOT FROM COURSE MATERIAL: used for waiting
from datetime import datetime  # NOT FROM COURSE MATERIAL: current date and time

import scooter_api
import zones

HISTORY_FILE = 'data/history.csv'


def collect_once():
    # load the live scooters and count them per zone
    scooters = scooter_api.fetch_scooters()
    counts = zones.count_per_zone(scooters)

    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M')  # NOT FROM COURSE MATERIAL

    # one line per zone, built with a list comprehension and f-strings
    lines = [f'{timestamp},{now.weekday()},{now.hour},{zone},{count}\n'
             for zone, count in counts.items()]

    # NOT FROM COURSE MATERIAL: open the file in "append" mode and add the lines
    with open(HISTORY_FILE, 'a') as file:
        file.writelines(lines)

    print(f'{timestamp}: saved {len(scooters)} scooters')


def run(every_minutes=30):
    # repeat forever: collect, then wait
    while True:
        collect_once()
        time.sleep(every_minutes * 60)


run()
