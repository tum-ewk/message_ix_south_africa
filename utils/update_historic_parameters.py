import pandas as pd
import ixmp
import message_ix
from itertools import product

# define database and the baseline scenario
model = 'MESSAGE South Africa'
baseline = 'baseline'
database = 'message_sa'

mp = ixmp.Platform(dbprops=f'./db/{database}', dbtype='HSQLDB')
base = message_ix.Scenario(mp, model=model, scenario=baseline)
fixed = base.clone(model, 'baseline', keep_solution=False)
all_years = [int(i) for i in fixed.set('year')]
hist_years = [int(i) for i in all_years if int(i) < 2010]

for _par in ['output', 'input', 'fix_cost', 'var_cost', 'construction_time', 'technical_lifetime', 'capacity_factor',
             'operation_factor', 'min_utilization_factor', 'emission_factor']:
    for tec in fixed.set('technology'):
        try:
            life_time = fixed.par('technical_lifetime', {'technology': tec}).value[0]
            relevant_years = [i for i in list(product(hist_years, all_years)) if i[0] < i[1] <= i[0] + life_time]
            relevant_years_vtg = [i[0] for i in relevant_years]
            relevant_years_act = [i[1] for i in relevant_years]
        except IndexError:
            life_time = 1
            relevant_years_vtg=hist_years
            relevant_years_act=hist_years
        try:
            par = fixed.par(_par, {'technology': tec})
            new_par = pd.DataFrame(columns=par.columns, index=range(0, len(relevant_years_vtg)))
            new_par = new_par.assign(year_vtg=relevant_years_vtg, year_act=relevant_years_act)
            for col in [i for i in par.columns if i not in ['year_vtg', 'year_act']]:
                kwargs = {col: lambda x: par.loc[0, col]}
                new_par = new_par.assign(**kwargs)
            fixed.check_out()
            fixed.add_par(_par, new_par)
            fixed.commit('add missing output')
        except KeyError:
            pass
fixed.solve(model='MESSAGE-MACRO')
fixed.set_as_default()
mp.close_db()
