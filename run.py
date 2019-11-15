# define database and the baseline scenario
import numpy as np

from utils.pp_plot_emissions import plot_emissions
from utils.pp_plot_gas_use import plot_gas_use
from utils.pp_plot_heatmaps import plot_heatmap_comparison
from utils.pp_plot_power_sector import plot_power_sector
from utils.pp_result_to_iamc import results_to_xlsx
from utils.run_scenarios import run_scenarios

model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

# shale gas extraction costs (USDpGJ) & carbon costs (USDtCO2) to model
# shale_cost = list(range(1, 32, 2)) + [10000]
# carbon_cost = list(range(0, 62, 2))
# shale_cost = list(set([0.3, 0.5, 1, 3, 1000] + list(range(1, 32, 2)) + [10000]))
# carbon_cost = list(set([0, 1, 3, 7, 10, 15, 30, 60] + list(range(0, 62, 2))))
shale_cost = sorted(list(set([0.3, 0.5, 1, 3, 10000] + [round(i, 1) for i in np.arange(0.3, 8, 0.4)] + [10000])))
carbon_cost = list(set([0, 1, 3, 7, 10, 15, 30, 60] + list(range(0, 62, 2))))

# run the scenarios
run_scenarios(model, baseline, database, shale_cost, carbon_cost)

# run the postprocessing
results_to_xlsx(model, baseline, database, shale_cost, carbon_cost)

# plot ghg-emissions over the model horizon
plot_emissions(c=[0, 1, 3, 7, 15, 30, 60])

# plot energy and capacity mix of the power sector
plot_power_sector(s=[1, 3, 10000], c=[0, 10, 30], order=[(10000, 0), (10000, 10), (10000, 30),
                                                         (3, 0), (3, 10), (3, 30), (1, 0), (1, 10), (1, 30)])

# plot energy and capacity mix of the power sector
plot_gas_use(s=[1, 3, 10000], c=[0, 10, 30], order=[(10000, 0), (10000, 10), (10000, 30),
                                                    (3, 0), (3, 10), (3, 30), (1, 0), (1, 10), (1, 30)])

# plot the scenario analysis heat maps - the variable 'years' indicates which years are presented in the plot
plot_heatmap_comparison(years=[2030])
plot_heatmap_comparison(years=[2050])
plot_heatmap_comparison(years=[2020, 2030, 2040, 2050])
