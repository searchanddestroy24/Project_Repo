# app.py
# Owner: Role 4 (App & Visualisation), integration by Role 1
#
# ScooterSpot St. Gallen: the Streamlit web app.
# Start it from the project folder with:   streamlit run app.py
#
# Structure (same building blocks as streamlit_demo_full.py from Unit 4):
#   1. page configuration and sidebar
#   2. "Right now": live e-scooters per zone from the API
#   3. "Plan ahead": prediction from our own model for a chosen weekday and hour

import streamlit as st

import scooter_api
import zones
import model

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# ---------------------------------------------------------------------------
# 1. Page configuration and sidebar
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
    FCS group project, HSG
    ''')

st.title('ScooterSpot St. Gallen')
st.header('Will there be an e-scooter near me? :scooter:', divider='rainbow')
st.write('''
    **Problem:** you leave home at 07:45 to reach a lecture at HSG and plan to take an
    e-scooter, but when you arrive there is none nearby. ScooterSpot shows how many
    e-scooters are in your zone right now and predicts how many there will usually be
    on the weekday and hour you choose, so you can plan ahead.
    ''')

# the zone is chosen once and used in both parts of the app
chosen_zone = st.selectbox('Your zone', list(zones.ZONES.keys()))

# ---------------------------------------------------------------------------
# 2. Right now: live data from the API
# ---------------------------------------------------------------------------
st.header('Right now', divider='gray')

show_raw_data = st.toggle('show live results as raw data', value=False)

if st.button('Load live e-scooters'):
    # NOT FROM COURSE MATERIAL: try/except keeps the app running if the API is down
    try:
        scooters = scooter_api.fetch_scooters()
    except Exception as error:
        st.write(f':warning: The API could not be reached ({error}). Please try again later.')
        scooters = []
    counts = zones.count_per_zone(scooters)

    st.write(f'**{counts[chosen_zone]}** e-scooters are in the zone **{chosen_zone}** '
             f'right now ({len(scooters)} in the whole search area).')

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(counts)
    with col2:
        if show_raw_data:
            st.write(counts)
        else:
            st.data_editor(counts)

# ---------------------------------------------------------------------------
# 3. Plan ahead: prediction with our own model
# ---------------------------------------------------------------------------
st.header('Plan ahead', divider='gray')

history = model.load_history()

# Walking skeleton: as long as no real data exists, fall back to the FAKE sample
# data so that the model and the charts can already be developed and tested.
if len(history) == 0:
    history = model.load_history(model.SAMPLE_FILE)
    if len(history) > 0:
        st.write(':warning: **Using FAKE sample data** (data/sample_history.csv). '
                 'Real predictions appear as soon as `collector.py` has created data/history.csv.')

if len(history) == 0:
    st.write('No data yet. Run `python make_sample_data.py` (fake test data) '
             'or `python collector.py` (real data).')
else:
    # train on the older data, keep the newest data to test the model
    training_data, test_data = model.split_history(history)
    trained_model = model.train_model(training_data)

    col3, col4 = st.columns(2)
    with col3:
        weekday_name = st.selectbox('Weekday', WEEKDAYS)
    with col4:
        hour = st.number_input('Hour (0-23)', value=8, min_value=0, max_value=23)

    weekday = WEEKDAYS.index(weekday_name)  # 'Monday' -> 0, 'Tuesday' -> 1, ...
    prediction = model.predict(trained_model, chosen_zone, weekday, hour)

    if prediction is None:
        st.write('We have no data for this zone and hour yet.')
    else:
        st.write(f'On a typical **{weekday_name}** at **{hour}:00** there are about '
                 f'**{prediction:.1f}** e-scooters in the zone **{chosen_zone}**.')
        if prediction < 1:
            st.write('That is less than one scooter: better plan to walk or take the bus.')

    # predicted number of scooters for every hour of the chosen day
    st.write(f'Predicted e-scooters in {chosen_zone} over the day ({weekday_name}):')
    day_curve = {}
    for h in range(24):
        value = model.predict(trained_model, chosen_zone, weekday, h)
        if value is not None:
            day_curve[h] = value
    st.bar_chart(day_curve)

    # how good is the model? (needed for the video / Q&A)
    error = model.evaluate(trained_model, test_data)
    if error is not None:
        st.write(f'Model check: trained on {len(training_data)} rows, tested on '
                 f'{len(test_data)} newer rows. On average the prediction is off by '
                 f'{error:.2f} scooters.')
