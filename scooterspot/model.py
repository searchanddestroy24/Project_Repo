# model.py
# Owner: Role 3 (Machine Learning)
#
# Our own machine learning model: it learns from the collected history how many
# e-scooters are usually available in a zone on a given weekday and hour.
#
# Training = for every (zone, weekday, hour) combination, compute the average
#            number of scooters seen in the history.
# Usage    = look up the learned average for the combination the user asks for.
#
# This follows the lecture idea (Unit 2, "A brief intro to Machine Learning"):
# historic features (zone, weekday, hour) + historic target (number of scooters)
# -> train a model -> predict the target for new inputs.
#
# Course concepts used: dictionaries with tuple keys, lists, slicing,
# for loops, statistics.mean, glob, split(), int().

import glob
import statistics

HISTORY_FILE = 'data/history.csv'          # real data, written by collector.py
SAMPLE_FILE = 'data/sample_history.csv'    # FAKE data for development only


def load_history(filename=HISTORY_FILE):
    # Reads data/history.csv and returns a list of tuples
    # (weekday, hour, zone, count). Returns [] if the file does not exist yet.
    if not glob.glob(filename):
        return []

    # NOT FROM COURSE MATERIAL: open the file and read all of its text
    with open(filename) as file:
        text = file.read()

    history = []
    for line in text.splitlines():
        parts = line.split(',')
        if len(parts) == 5:
            timestamp, weekday, hour, zone, count = parts
            history.append((int(weekday), int(hour), zone, int(count)))
    return history


def split_history(history, test_share=0.2):
    # The newest rows are used for testing, the older rows for training.
    # (The file is in time order, so the end of the list is the newest data.)
    split_index = int(len(history) * (1 - test_share))
    return history[:split_index], history[split_index:]


def train_model(training_data):
    # Step 1: group all observed counts by (zone, weekday, hour)
    groups = {}
    for weekday, hour, zone, count in training_data:
        key = (zone, weekday, hour)
        if key in groups:
            groups[key].append(count)
        else:
            groups[key] = [count]

    # Step 2: the "model" is the average count for every group
    model = {}
    for key, counts in groups.items():
        model[key] = statistics.mean(counts)
    return model


def predict(model, zone, weekday, hour):
    # Returns the predicted number of scooters, or None if we have never
    # seen this combination.
    key = (zone, weekday, hour)
    if key in model:
        return model[key]

    # Fallback: no data for this exact weekday -> average over all weekdays
    # at the same hour in the same zone.
    same_hour = [value for (z, d, h), value in model.items() if z == zone and h == hour]
    if len(same_hour) > 0:
        return statistics.mean(same_hour)
    return None


def evaluate(model, test_data):
    # Mean absolute error: on average, how many scooters is the prediction off?
    errors = []
    for weekday, hour, zone, count in test_data:
        prediction = predict(model, zone, weekday, hour)
        if prediction is not None:
            errors.append(abs(prediction - count))
    if len(errors) == 0:
        return None
    return statistics.mean(errors)
