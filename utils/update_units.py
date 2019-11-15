import ixmp
import message_ix

model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
base = message_ix.Scenario(mp, model=model, scenario=baseline)
fixed = base.clone(model, 'baseline', keep_solution=False)
if fixed.has_solution():
    fixed.remove_solution()

par_list = fixed.par_list()

unit_dict = {'demand': 'GWa/a',
             'resource_remaining': '-',
             'resource_volume': 'GWa',
             'technical_lifetime': 'year',
             'capacity_factor': '-',
             'min_utilization_factor': '-',
             'inv_cost': 'USD/kW',
             'fix_cost': 'USD/kW/a',
             'var_cost': 'USD/kWa',
             'output': '-',
             'input': '-',
             'bound_new_capacity_up': 'GW/a',
             'bound_total_capacity_up': 'GW',
             'bound_activity_up': 'GWa/a',
             'bound_activity_lo': 'GWa/a',
             'initial_new_capacity_up': 'GW/a',
             'growth_new_capacity_up': '-',
             'growth_new_capacity_lo': '-',
             'initial_activity_up': 'GWa/a',
             'growth_activity_up': '-',
             'growth_activity_lo': '-',
             'emission_factor': 'MtCO2eq/GWa',
             'construction_time': 'year',
             'renewable_potential': 'GWa/a',
             'renewable_capacity_factor': '-',
             'reliability_factor': '-',
             'peak_load_factor': '-',
             'flexibility_factor': '-',
             'rating_bin': '-',
             'emission_scaling': '-',
             'tax_emission': 'USD/tCO2',
             'relation_cost': 'USD/kWa',
             'relation_activity': 'GWa/a',
             'duration_period': 'year',
             'duration_time': '-',
             'interestrate': '-',
             'historical_new_capacity': 'GW/a',
             'historical_activity': 'GWa/a',
             'historical_gdp': 'TUSD',
             'MERtoPPP': '-',
             'aeei': '-',
             'cost_MESSAGE': 'MUSD/a',
             'demand_MESSAGE': 'GWa/a',
             'depr': '-',
             'drate': '-',
             'esub': '-',
             'gdp_calibrate': 'TUSD',
             'grow': '-',
             'kgdp': '-',
             'kpvs': '-',
             'lakl': '-',
             'lotol': '-',
             'p_ref': '-',
             'prfconst': '-',
             'price_MESSAGE': 'USD/kWa'
             }

fixed.check_out()
for par in par_list:
    _par = fixed.par(par)
    if not _par.empty:
        if not unit_dict[par] in mp.units():
            mp.add_unit(unit_dict[par])
        _par = _par.assign(unit=unit_dict[par])
        fixed.add_par(par, _par)
fixed.commit('update units')

fixed.solve(model='MESSAGE-MACRO')
fixed.set_as_default()
mp.close_db()
