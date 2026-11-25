"""
check_setup.py
Owner: Role 1 (Project lead)

Everyone runs this once after cloning the repository:   python check_setup.py
It tests every part of the app step by step. If a step fails, the error
appears directly below the step that broke.
"""

print('Step 1/5: importing libraries and our modules ...')
import database
import model
import scooter_api
import zones
print('   OK')

print('Step 2/5: calling the sharedmobility.ch API ...')
first_page = scooter_api.fetch_page(0)
print(f'   OK, the first page has {len(first_page)} items')
print('   Raw data of the first item (Role 2: check the keys "geometry", "x", "y"!):')
print('  ', first_page[:1])

print('Step 3/5: counting scooters per zone ...')
scooters = scooter_api.fetch_scooters()
print(f'   OK, {len(scooters)} scooters found: {zones.count_per_zone(scooters)}')

print('Step 4/5: reading the databases ...')
real = database.load_observations(database.REAL_DB)
sample = database.load_observations(database.SAMPLE_DB)
print(f'   OK, {len(real)} real rows, {len(sample)} FAKE sample rows')
if len(sample) == 0:
    print('   -> run "python make_sample_data.py" first')

print('Step 5/5: training and comparing the models on the sample data ...')
best_model, best_name, comparison, test_metrics = model.train_and_compare(sample)
print(comparison.round(3))
print(f'   OK, best model: {best_name}, test accuracy {test_metrics["accuracy"]:.2f}')

print('\nAll steps passed. Now start the app with:   streamlit run app.py')
