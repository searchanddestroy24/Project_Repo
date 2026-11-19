# ScooterSpot St. Gallen

FCS group project (HSG), built with Python and Streamlit.

## Problem
Students and commuters in St. Gallen plan to take a shared e-scooter, but often find none
nearby when they need one (e.g. at 07:45 before a lecture). ScooterSpot shows how many
e-scooters are in your zone **right now** and **predicts** how many there will usually be
on a chosen weekday and hour.

## How the app meets the course requirements
| # | Requirement | Where |
|---|-------------|-------|
| 1 | Problem clearly stated | top of `app.py`, this README, video |
| 2 | Data loaded via API | `scooter_api.py` (sharedmobility.ch API of the BFE) |
| 3 | Visualisation | bar charts in `app.py` |
| 4 | User interaction | zone/weekday selection, hour input, button, toggle |
| 5 | Own machine learning model | `model.py` (trained on our own collected data) |
| 6 | Source code commented | all `.py` files |
| 7 | Contribution matrix + GenAI reflection | video (see `ROLES.md`) |
| 8 | 4-minute video, own voice | see `ROLES.md` |

## Files
| File | What it does |
|------|--------------|
| `app.py` | the Streamlit web app |
| `scooter_api.py` | loads live e-scooter positions from the API |
| `zones.py` | defines the zones and counts scooters per zone |
| `collector.py` | asks the API every 30 min and saves the counts to `data/history.csv` |
| `model.py` | trains and evaluates the prediction model |
| `make_sample_data.py` | creates FAKE test data for development only |
| `check_setup.py` | tests every part of the app step by step |
| `data/history.csv` | our collected dataset (created by `collector.py`) |

## Walking skeleton: day-1 checklist
The skeleton is the thinnest version of the app that already runs end to end:
**API → zones → collected data → model → Streamlit app → online**.
Every part is basic, but connected. From here, each role improves its own part
without blocking the others.

- [ ] Role 1 puts the repo on GitHub and invites everyone
- [ ] Everyone: `git clone ...`, then `pip install -r requirements.txt`
- [ ] Everyone: `python check_setup.py` passes all 4 steps
- [ ] Everyone: `streamlit run app.py` opens the app in the browser
- [ ] Role 2: API keys checked, `python collector.py` is running
- [ ] Role 1: app deployed once on share.streamlit.io

## Run it
```
pip install -r requirements.txt
python make_sample_data.py # FAKE test data, so the model works from day 1
python check_setup.py      # tests every part step by step
python collector.py        # start collecting REAL data (keep it running)
streamlit run app.py       # in a second terminal: start the app
```

As soon as `data/history.csv` exists, the app uses the real data instead of the
fake sample data. **Delete `data/sample_history.csv` before the final submission.**

## Data source
Source: BFE (Swiss Federal Office of Energy), sharedmobility.ch.
Open data, free use, source must be credited.
API documentation: https://github.com/SFOE/sharedmobility

## Code from outside the course material
Lines marked `NOT FROM COURSE MATERIAL` use things not covered in the lectures/exercises
so far (reading/writing files, `response.json()`, `datetime`, `time.sleep`).
Everything else uses only concepts from Units 1-4.
