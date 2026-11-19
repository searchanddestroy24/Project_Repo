# make_sample_data.py
# Owner: Role 3 (Machine Learning)
#
# Creates FAKE sample data in data/sample_history.csv so that the whole app
# (including the model) can be developed and tested before real data exists.
#
#   !!! These numbers are random. They must NOT be used in the final app or video. !!!
#
# Run once with:   python make_sample_data.py
#
# Course concepts used: random.randrange (roll the dice), for loops, range,
# lists, f-strings, if/else.

import random

import zones

SAMPLE_FILE = 'data/sample_history.csv'


def fake_count(hour):
    # a little bit of realism: more scooters during the day than at night
    if 7 <= hour <= 19:
        return random.randrange(2, 9)
    return random.randrange(0, 4)


def make_sample_data(days=7):
    lines = []
    zone_names = list(zones.ZONES.keys()) + ['Other']
    for day in range(days):
        weekday = day % 7
        for hour in range(24):
            for zone in zone_names:
                timestamp = f'SAMPLE day {day + 1} {hour:02d}:00'
                lines.append(f'{timestamp},{weekday},{hour},{zone},{fake_count(hour)}\n')

    # NOT FROM COURSE MATERIAL: write all lines into a new file
    with open(SAMPLE_FILE, 'w') as file:
        file.writelines(lines)
    print(f'wrote {len(lines)} FAKE rows to {SAMPLE_FILE}')


make_sample_data()
