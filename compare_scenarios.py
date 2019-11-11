import pandas as pd

from utils.run_scenarios import *

# define database and the baseline scenario
model = 'MESSAGE South Africa'
baseline = 'baseline'
fixed_basleine = 'baseline_fixed_output'
database = 'message_sa'

mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
base = message_ix.Scenario(mp, model=model, scenario=baseline)
fixed = message_ix.Scenario(mp, model=model, scenario=fixed_basleine)

if not base.has_solution():
    base.solve(model='MESSAGE-MACRO')
if not fixed.has_solution():
    fixed.solve(model='MESSAGE-MACRO')

# compare scenario results
CAP_NEW_old: pd.DataFrame = base.var('CAP_NEW').groupby(['node_loc', 'technology']).sum().reset_index()
CAP_NEW_old = CAP_NEW_old[['node_loc', 'technology', 'lvl']]
CAP_NEW_fixed: pd.DataFrame = fixed.var('CAP_NEW').groupby(['node_loc', 'technology']).sum().reset_index()
CAP_NEW_fixed = CAP_NEW_fixed[['node_loc', 'technology', 'lvl']]

CAP_NEW_diff = CAP_NEW_fixed.merge(CAP_NEW_old, how='outer', on=['node_loc', 'technology'])
CAP_NEW_diff['lvl'] = CAP_NEW_diff['lvl_x'].subtract(CAP_NEW_diff['lvl_y'])
CAP_NEW_diff = CAP_NEW_diff[CAP_NEW_diff['lvl'] != 0]
CAP_NEW_diff['rel_tech_diff'] = CAP_NEW_diff['lvl'].divide(CAP_NEW_diff['lvl_x']) * 100
CAP_NEW_diff['rel_total_diff'] = CAP_NEW_diff['lvl'].divide(base.var('CAP', {'year_act': 2050})['lvl'].sum()) * 100

EMISS_old: pd.DataFrame = base.var('EMISS', {'emission': 'CO2', 'node': 'South Africa'})['lvl'].sum()
EMISS_fixed: pd.DataFrame = fixed.var('EMISS', {'emission': 'CO2', 'node': 'South Africa'})['lvl'].sum()
EMISS_diff = (EMISS_fixed-EMISS_old)/EMISS_fixed * 100