from utils.pp_db_to_xlsx import results_to_xlsx
from utils.pp_plot_emissions import plot_emissions
from utils.pp_plot_heatmaps import plot_heatmap_comparison
from utils.pp_plot_power_sector import plot_power_sector
from utils.run_scenarios import *

# define database and the baseline scenario
model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

# shale gas extraction costs (USDpMWh) & carbon costs (USDtCO2) to model
# shale_cost = list(range(1, 32, 2)) + [10000]
# carbon_cost = list(range(0, 62, 2))
shale_cost = [1, 10, 30, 1000]
carbon_cost = [0, 5, 15, 30]

# run the scenarios
run_scenarios(model, baseline, database, shale_cost, carbon_cost)

# run the postprocessing
results_to_xlsx(model, baseline, database, shale_cost, carbon_cost)

# plot ghg-emissions over the model horizon
plot_emissions()

# plot energy and capacity mix of the power sector
plot_power_sector()

# plot the scenario analysis heat maps - the variable 'years' indicates
# which years are presented in the plot
plot_heatmap_comparison(years=[2050])
