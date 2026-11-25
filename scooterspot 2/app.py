"""
app.py
Owner: Role 4 (App & Visualisation), integration by Role 1

ScooterSpot St. Gallen - the Streamlit web app.
Start it from the project folder:   streamlit run app.py

Structure:
    1. page configuration, sidebar, problem statement
    2. "Right now":   live e-scooters from the API, on a map and per zone
    3. "Plan ahead":  prediction of our own ML model for a chosen weekday and hour
    4. "How good is our model?": model comparison and test results

Course concepts: st.set_page_config, st.sidebar, st.title, st.header, st.columns,
st.selectbox, st.number_input, st.toggle, st.button, st.bar_chart, st.write
(Unit 4 streamlit_demo_full.py), st.dataframe and pandas (Unit 7 streamlit_db_demo.py).
"""

import pandas as pd
import streamlit as st

import database
import model
import scooter_api
import zones

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MIN_REAL_ROWS = 200   # below this, the real data is too small to train a model

# ---------------------------------------------------------------------------
# 1. Page configuration, sidebar, problem statement
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title='ScooterSpot St. Gallen',
    page_icon=':scooter:',
    layout='centered',
    initial_sidebar_state='auto',
)

st.sidebar.write('''
    ## About ScooterSpot
    Find out whether an e-scooter is available near you in St. Gallen,
    now and at the time you plan to leave.

    ## Data source
    Source: BFE, [sharedmobility.ch](https://www.sharedmobility.ch)

    ## Team
    FCS group project, University of St. Gallen
    ''')

st.title('ScooterSpot St. Gallen')
st.header('Will there be an e-scooter near me? :scooter:', divider='rainbow')
st.write('''
    **Problem:** you leave home at 07:45 to reach a lecture at HSG and plan to take an
    e-scooter, but when you arrive there is none nearby. ScooterSpot shows where the
    e-scooters are right now and predicts how likely it is to find one in your zone
    on the weekday and hour you choose, so you can plan ahead.
    ''')

zone_names = [zone.name for zone in zones.ZONES]
chosen_zone = zones.ZONES_BY_NAME[st.selectbox('Your zone', zone_names)]

# ---------------------------------------------------------------------------
# 2. Right now: live data from the API
# ---------------------------------------------------------------------------
st.header('Right now', divider='gray')

if st.button('Load live e-scooters'):
    # EXTERNAL: try/except (Python docs, "Errors and Exceptions") keeps the app
    # running if the API is not reachable
    try:
        scooters = scooter_api.fetch_scooters()
    except Exception as error:
        st.write(f':warning: The API could not be reached ({error}). Please try again later.')
        scooters = []

    counts = zones.count_per_zone(scooters)
    st.write(f'**{counts[chosen_zone.name]}** e-scooters are in the zone **{chosen_zone.name}** '
             f'right now ({len(scooters)} in the whole search area).')

    if len(scooters) > 0:
        # EXTERNAL: st.map (Streamlit docs) draws points from the columns 'lat' and 'lon'
        st.map(pd.DataFrame(scooters, columns=['lat', 'lon']))
    st.bar_chart(counts)

# ---------------------------------------------------------------------------
# 3. Plan ahead: prediction with our own ML model
# ---------------------------------------------------------------------------
st.header('Plan ahead', divider='gray')


# EXTERNAL: st.cache_resource (Streamlit docs on caching, linked in the course's
# streamlit_db_demo.py) trains the models only once instead of on every click.
@st.cache_resource
def get_trained_model(use_sample):
    if use_sample:
        observations = database.load_observations(database.SAMPLE_DB)
    else:
        observations = database.load_observations(database.REAL_DB)
    return model.train_and_compare(observations)


real_rows = len(database.load_observations(database.REAL_DB))
use_sample = real_rows < MIN_REAL_ROWS
if use_sample:
    st.write(f':warning: **Using FAKE sample data.** Only {real_rows} real rows collected so far; '
             f'the app switches to real data at {MIN_REAL_ROWS} rows.')

best_model, best_name, comparison, test_metrics = get_trained_model(use_sample)

col1, col2 = st.columns(2)
with col1:
    weekday_name = st.selectbox('Weekday', WEEKDAYS)
with col2:
    hour = st.number_input('Hour (0-23)', value=8, min_value=0, max_value=23)
weekday = WEEKDAYS.index(weekday_name)

predicted_class, probability_any = model.predict_availability(
    best_model, chosen_zone.zone_id, weekday, hour)

st.write(f'On a **{weekday_name}** at **{hour}:00** in **{chosen_zone.name}** we expect: '
         f'**{model.CLASS_NAMES[predicted_class]}**.')
st.write(f'Chance of finding at least one e-scooter: **{probability_any:.0%}**')

# chance of finding a scooter for every hour of the chosen day
day_curve = {}
for h in range(24):
    cls, probability = model.predict_availability(best_model, chosen_zone.zone_id, weekday, h)
    day_curve[h] = probability
st.write(f'Chance of at least one e-scooter in {chosen_zone.name} over the day ({weekday_name}):')
st.bar_chart(day_curve)

# ---------------------------------------------------------------------------
# 4. How good is our model? (for the video and the Q&A)
# ---------------------------------------------------------------------------
st.header('How good is our model?', divider='gray')

if st.toggle('show model comparison', value=False):
    st.write('Validation results of all models (sorted by F1, macro average):')
    st.dataframe(comparison.round(3))
    st.write(f'Best model: **{best_name}**. On the unseen test data it reaches an accuracy of '
             f'**{test_metrics["accuracy"]:.2f}** and an F1 score of **{test_metrics["f1"]:.2f}**.')
