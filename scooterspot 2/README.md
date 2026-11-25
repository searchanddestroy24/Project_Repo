# ScooterSpot St. Gallen

FCS group project (HSG), built with Python and Streamlit.

## Problem
Students and commuters in St. Gallen plan to take a shared e-scooter, but often find none
nearby when they need one (e.g. at 07:45 before a lecture). ScooterSpot shows where the
e-scooters are **right now** and **predicts** how likely it is to find one in a zone on a
chosen weekday and hour.

## How the app meets the grading requirements
| # | Requirement | Where |
|---|-------------|-------|
| 1 | Problem clearly stated | top of `app.py`, this README, video |
| 2 | Data via API **and** database | `scooter_api.py` (sharedmobility.ch API) + `database.py` (SQLite) |
| 3 | Visualisation | map of live scooters, bar charts, model comparison table |
| 4 | User interaction | zone/weekday selection, hour input, button, toggle |
| 5 | Own machine learning model | `model.py`: 4 classifiers + baseline compared, best one used |
| 6 | Source code commented | every `.py` file |
| 7 | Contribution matrix + GenAI reflection | video (templates in `ROLES.md`) |
| 8 | 4-minute video, own voice | see `ROLES.md` |

## Architecture (walking skeleton)
```
sharedmobility.ch API --> scooter_api.py --> zones.py --> collector.py --> data/scooters.db
                                  |                                              |
                                  v                                              v
                     app.py "Right now" (map)              model.py (train + compare classifiers)
                                                                                 |
                                                                                 v
                                                             app.py "Plan ahead" (prediction)
```

## Files
| File | What it does | Owner |
|------|--------------|-------|
| `app.py` | the Streamlit web app | Role 4 |
| `scooter_api.py` | loads live e-scooter positions from the API | Role 2 |
| `zones.py` | `Zone` class, zones of St. Gallen, counting per zone | Role 2 |
| `database.py` | saves and loads observations in SQLite | Role 2 |
| `collector.py` | asks the API every 30 min and saves the counts | Role 2 |
| `model.py` | trains, compares and evaluates the classifiers | Role 3 |
| `make_sample_data.py` | creates FAKE test data (development only) | Role 3 |
| `check_setup.py` | tests every part step by step | Role 1 |
| `data/scooters.db` | our real collected data | Role 2 |
| `data/sample.db` | FAKE data, **delete before submission** | Role 3 |

## Run it
```
pip install -r requirements.txt
python make_sample_data.py   # FAKE test data, so the model works from day 1
python check_setup.py        # tests every part step by step
python collector.py          # start collecting REAL data (keep it running)
streamlit run app.py         # in a second terminal: start the app
```
The app uses the fake sample data until `data/scooters.db` holds at least 200 real rows
(about one day of collecting), then switches to the real data automatically.

## Where our code comes from
Almost everything is taken from the course material:

| Technique | Course source |
|-----------|---------------|
| Streamlit layout, widgets, `st.bar_chart` | Unit 4 `streamlit_demo_full.py` |
| `st.dataframe`, pandas + SQLite in Streamlit | Unit 7 `streamlit_db_demo.py` |
| `requests.get`, `status_code`, `response.json()` | Unit 6 `poke-api-client.py`, Assignment 6 |
| Request parameters as a dictionary | Assignment 6 (hints) |
| Classes, `__init__`, methods, `__str__` | Unit 5, Assignment 5 |
| `sqlite3`, `CREATE TABLE`, `INSERT`, `with DB:`, `?` parameters | Unit 7, Assignment 7 |
| `pd.read_sql`, DataFrames, `value_counts`, `sort_values` | Unit 7/8, Assignments 7-9 |
| `datetime.now()`, `strftime`, `time` module | Assignments 5 and 6 |
| `train_test_split` (stratified, seed), several classifiers, accuracy/precision/recall/F1 | Assignments 10 and 11 |
| `KNeighborsClassifier` | Assignment 10 |

**Third-party / external additions** (not in the course material, marked `EXTERNAL` in the code):

| What | Why | Source |
|------|-----|--------|
| sharedmobility.ch API | our data source | https://github.com/SFOE/sharedmobility |
| `st.map` | map of live scooters | Streamlit docs (https://docs.streamlit.io), API reference: `st.map` |
| `@st.cache_resource` | train the models once, not on every click | Streamlit docs on caching (linked in `streamlit_db_demo.py`) |
| `try` / `except` | app keeps running if the API is down | Python docs, "Errors and Exceptions" |
| `time.sleep` | wait between two collections | Python docs, module `time` |
| `predict_proba` | probability of finding a scooter | scikit-learn docs of the classifiers |
| Decision Tree, Random Forest, Logistic Regression | candidates for the model comparison | scikit-learn docs (Assignment 11 asks to pick models yourself) |

## Data source
Source: BFE (Swiss Federal Office of Energy), sharedmobility.ch. Open data, free use, source must be credited.
