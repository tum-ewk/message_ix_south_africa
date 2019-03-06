import ixmp
import message_ix
from itertools import product


def run_scenarios(model, baseline, database, shale_costs, carbon_costs):
    # launch a platform to access the database
    mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
    base = message_ix.Scenario(mp, model=model, scenario=baseline)
    base.solve(model='MESSAGE-MACRO')
    
    # Define values for progress report
    num = len(list(product(shale_costs, carbon_costs)))
    i = 0
    infeasible_models = []

    # Run Scenario
    ##################################
    for s, c in product(shale_costs, carbon_costs):

        scenario = f'{s}USDpMWh-{c}USDtCO2'
        scen = base.clone(model, scenario, keep_solution=False)
        scen.set_as_default()
        scen.check_out()
        year = base.set('year').astype(int)
        first_model_year = scen.cat('year', 'firstmodelyear')
        model_years = list(year[year >= int(first_model_year)])

        # update scenario carbon cost
        filters = dict(node='South Africa', type_emission='CO2',
                       type_tec='all', type_year=model_years)
        par = scen.par('tax_emission', filters)
        par['value'] = [(c * ((1 + 0.05) ** n)) for n in range(0, 60, 10)]
        scen.add_par('tax_emission', par)

        # update scenario shale gas extraction costs
        filters = dict(mode='M1', node_loc='South Africa', time='year',
                       year_act=model_years, year_vtg=model_years,
                       technology='shale_extr')
        par = scen.par('var_cost', filters)
        par['value'] = s * 8.76  # from USD/kWh to MUSD/GWa
        scen.add_par('var_cost', par)

        scen.commit('update variable costs and carbon price according to the '
                    'scenario specifications')

        # Solve Model
        try:
            scen.solve(model='MESSAGE-MACRO')
        except:
            infeasible_models = infeasible_models + [scenario]
            print(f'Infeasible model. Shale gas extraction costs: {s}, '
                  f'carbon price {c}.')
            continue
        print(f'Done running {i + 1} out of {num} scenarios.')
        i = i + 1

    mp.close_db()
    print(f'The following scenarios are infeasible: {infeasible_models}')
