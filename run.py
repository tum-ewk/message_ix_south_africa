from utils.run_scenarios import *

# define database and the baseline scenario
model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

# shale gas extraction costs (USDpMWh) & carbon costs (USDtCO2) to model
shale_cost = list(range(1, 32, 2)) + [10000]
carbon_cost = list(range(0, 62, 2))

# run the scenarios
run_scenarios(model, baseline, database, shale_cost, carbon_cost)
