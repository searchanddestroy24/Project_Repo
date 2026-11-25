"""
model.py
Owner: Role 3 (Machine Learning)

Our own machine learning model. It predicts how many e-scooters will be available
in a zone on a given weekday and hour, as one of three classes:

    0 = no scooter       1 = 1-2 scooters       2 = 3 or more scooters

Features (inputs):  zone_id, weekday, hour
Target (output):    availability class, computed from the counted scooters

Procedure (exactly as in Assignments 10 and 11):
    1. split the data into 80% training, 10% validation, 10% test (stratified, seed 13)
    2. train several classifiers on the training data
    3. compare them on the validation data (accuracy, precision, recall, F1)
    4. pick the best one and report its performance on the test data

Course concepts: pandas DataFrames (Unit 8, Assignments 8 and 9), scikit-learn
train_test_split, classifiers, accuracy_score and precision_recall_fscore_support
(Assignments 10 and 11), KNeighborsClassifier (Assignment 10, Task 2.2).
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

FEATURES = ['zone_id', 'weekday', 'hour']
TARGET = 'availability'
CLASS_NAMES = {0: 'no scooter', 1: '1-2 scooters', 2: '3 or more scooters'}
SEED = 13


def count_to_class(count):
    """Turns a number of scooters into an availability class (0, 1 or 2)."""
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    else:
        return 2


def prepare_data(observations):
    """Adds the target column to a copy of the observations DataFrame."""
    df = observations.copy()
    df[TARGET] = df['count'].apply(count_to_class)
    return df


def split_data(df):
    """80% train, 10% validation, 10% test, stratified with a fixed seed (Assignment 11, Task 1)."""
    X = df[FEATURES]
    y = df[TARGET]

    # stratify only works if every class appears at least twice
    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_rest, y_train, y_rest = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=stratify)

    stratify = y_rest if y_rest.value_counts().min() >= 2 else None
    X_val, X_test, y_val, y_test = train_test_split(
        X_rest, y_rest, test_size=0.5, random_state=SEED, stratify=stratify)

    return X_train, X_val, X_test, y_train, y_val, y_test


def candidate_models():
    """The classifiers we compare. Role 3: add more (Assignment 11 asks for at least 5)."""
    return {
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Decision Tree': DecisionTreeClassifier(max_depth=6, random_state=SEED),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=SEED),
        'Logistic Regression': LogisticRegression(max_iter=1000),
    }


def evaluate(y_true, y_pred):
    """Accuracy plus macro precision, recall and F1 (Assignment 10, Task 1.4)."""
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0)
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def train_and_compare(observations):
    """
    Trains all candidate models and compares them on the validation data.

    Returns:
        best_model    the trained classifier with the highest validation F1
        best_name     its name
        comparison    DataFrame with the validation metrics of every model
        test_metrics  metrics of the best model on the (unseen) test data
    """
    df = prepare_data(observations)
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)

    rows = []

    # Baseline: always predict the most frequent class of the training data.
    # A real model must be better than this, otherwise it has learned nothing.
    most_frequent = y_train.value_counts().idxmax()
    baseline_pred = [most_frequent] * len(y_val)
    row = evaluate(y_val, baseline_pred)
    row['model'] = 'Baseline (most frequent class)'
    rows.append(row)

    trained = {}
    for name, model in candidate_models().items():
        model.fit(X_train, y_train)
        trained[name] = model
        row = evaluate(y_val, model.predict(X_val))
        row['model'] = name
        rows.append(row)

    comparison = pd.DataFrame(rows).set_index('model').sort_values('f1', ascending=False)

    # the best real model (the baseline is not allowed to win)
    best_name = comparison.drop(index='Baseline (most frequent class)').index[0]
    best_model = trained[best_name]
    test_metrics = evaluate(y_test, best_model.predict(X_test))

    return best_model, best_name, comparison, test_metrics


def predict_availability(model, zone_id, weekday, hour):
    """
    Returns (predicted class, probability that at least one scooter is there).
    EXTERNAL: predict_proba() is not used in the assignments, see the scikit-learn
    documentation of the classifiers. It gives the probability of every class.
    """
    X = pd.DataFrame([[zone_id, weekday, hour]], columns=FEATURES)
    predicted_class = int(model.predict(X)[0])

    probabilities = model.predict_proba(X)[0]
    probability_none = 0.0
    for cls, probability in zip(model.classes_, probabilities):
        if cls == 0:
            probability_none = probability
    return predicted_class, 1 - probability_none
