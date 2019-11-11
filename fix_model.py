from utils.run_scenarios import *

# define database and the baseline scenario
model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
base = message_ix.Scenario(mp, model=model, scenario=baseline)
fixed = base.clone(model, 'baseline_fixed_output', keep_solution=False)
years = [int(i) for i in fixed.set('year') if int(i) < 2010]
fixed.check_out()
for _par in ['output', 'input', 'fix_cost', 'var_cost', 'construction_time', 'technical_lifetime', 'capacity_factor',
             'operation_factor', 'min_utilization_factor', 'emission_factor']:
    par = fixed.par(_par, {'year_vtg': 2010})
    for y in years:
        par['year_vtg'] = y
        fixed.add_par(_par, par)
fixed.commit('add missing output')
fixed.solve(model='MESSAGE-MACRO')
fixed.set_as_default()
