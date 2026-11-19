# check_setup.py
# Owner: Role 1 (Project lead)
#
# Everyone runs this once after cloning the repository:   python check_setup.py
# It goes through every part of the app step by step. If a step fails,
# the error appears right below the step that broke.
#
# Course concepts used: functions, print with f-strings, lists, slicing.

print('Step 1/4: importing our modules ...')
import scooter_api
import zones
import model
print('   OK')

print('Step 2/4: calling the sharedmobility.ch API ...')
first_page = scooter_api.fetch_page(0)
print(f'   OK, the first page has {len(first_page)} items')
print('   Raw data of the first item (Role 2: check the keys!):')
print('  ', first_page[:1])

print('Step 3/4: counting scooters per zone ...')
scooters = scooter_api.fetch_scooters()
print(f'   OK, {len(scooters)} scooters found: {zones.count_per_zone(scooters)}')

print('Step 4/4: training the model ...')
history = model.load_history()
source = 'real data (data/history.csv)'
if len(history) == 0:
    history = model.load_history(model.SAMPLE_FILE)
    source = 'FAKE sample data (data/sample_history.csv)'
training_data, test_data = model.split_history(history)
trained_model = model.train_model(training_data)
print(f'   OK, trained on {len(training_data)} rows of {source}')
print(f'   Mean absolute error on {len(test_data)} test rows: {model.evaluate(trained_model, test_data)}')

print('\nAll steps passed. Now start the app with:   streamlit run app.py')
