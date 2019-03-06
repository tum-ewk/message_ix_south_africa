import pandas as pd
from itertools import product
import ixmp
import message_ix
import os


def create_timeseries(data, name, s, c, groupby):
    ts = data.groupby([groupby, 'year'], as_index=False).sum()
    ts = pd.pivot_table(ts, columns='year', values='lvl').reset_index(
        drop=True)
    ts['variable'] = name
    ts['cost'] = s
    ts['tax'] = c
    return ts


def results_to_xlsx(model, baseline, database, shale_costs, carbon_costs,
                    l_year=2050):
    # Launch data base and load baseline
    mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
    base = message_ix.Scenario(mp, model=model, scenario=baseline)

    year = base.set('year').astype(int)
    f_mod_year = base.cat('year', 'firstmodelyear')
    years = list(year[(year >= int(f_mod_year)) & (year <= l_year)])

    columns = ['variable', 'tax', 'cost'] + years
    all_ts = pd.DataFrame(columns=columns)

    # retrieve data from scenarios
    ##################################
    for s, c in [('none', 0)] + list(product(shale_costs, carbon_costs)):
        if s == 'none':
            scen = base
        else:
            scenario = f'{s}USDpMWh-{c}USDtCO2'
            scen = message_ix.Scenario(mp, model=model, scenario=scenario)

        # EMISSION DATA
        data = scen.var('EMISS', {'node': 'South Africa', 'year': years}
                        ).drop(['type_tec', 'mrg'], axis=1)
        ts = create_timeseries(data, 'Emissions|Total', s, c, 'node')
        all_ts = all_ts.append(ts, sort=True)

        # POWER SECTOR DATA
        act_dic = {'Coal wo ccs': ['coal_adv', 'coal_ppl', 'igcc'],
                   'Coal ccs': ['coal_adv_ccs', 'igcc_ccs'],
                   'Gas wo ccs': ['gas_cc', 'gas_ct', 'gas_ppl'],
                   'Gas ccs': ['gas_cc_ccs'],
                   'Other ppls': ['foil_ppl', 'loil_ppl', 'elec_imp'],
                   'Renewable': ['wind_ppl', 'solar_th_ppl_base',
                                 'solar_th_ppl', 'hydro_ppl', 'solar_pv_ppl'],
                   'Nuclear': ['nuc_ppl']}

        for k, t in act_dic.items():
            data = scen.var('ACT', {'node_loc': 'South Africa',
                                    'year_act': years, 'technology': t})
            data = data.rename(columns={'year_act': 'year'})
            ts = create_timeseries(data, f'Activity|{k}', s, c, 'node_loc')
            all_ts = all_ts.append(ts, sort=True)

            data = scen.var('CAP', {'node_loc': 'South Africa',
                                    'year_vtg': years, 'technology': t})
            data = data.rename(columns={'year_vtg': 'year'})
            ts = create_timeseries(data, f'Capacity|{k}', s, c, 'node_loc')
            all_ts = all_ts.append(ts, sort=True)

        # ENERGY USE DATA
        act_dic = {'shale_extr': 'shale_extr', 'coal_extr': 'coal_extr',
                   'all_extr': ['shale_extr', 'coal_extr', 'gas_extr',
                                'oil_extr'],
                   'all_imp': ['coal_imp', 'gas_imp', 'oil_imp',
                               'loil_imp', 'foil_imp', 'elec_imp'],
                   'all_exp': ['coal_exp', 'gas_exp', 'oil_exp', 'loil_exp',
                               'foil_exp', 'elec_exp'],
                   'renewable_energy': ['solar_th_ppl_base', 'solar_i',
                                        'bio_extr', 'solar_rc', 'wind_ppl',
                                        'solar_pv_ppl', 'hydro_ppl',
                                        'solar_th_ppl']}

        for k, t in act_dic.items():
            data = scen.var('ACT', {'node_loc': 'South Africa',
                                    'year_act': years, 'technology': t})
            data = data.rename(columns={'year_act': 'year'})
            ts = create_timeseries(data, f'Activity|{k}', s, c, 'node_loc')
            all_ts = all_ts.append(ts, sort=True)

    all_ts = all_ts[columns]

    if not os.path.exists('results/'):
        os.makedirs('results/')

    all_ts.to_excel('results/timeseries.xlsx')
