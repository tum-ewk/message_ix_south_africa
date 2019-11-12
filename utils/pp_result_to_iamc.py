import os
from itertools import product

import ixmp
import message_ix
import pandas as pd


def create_timeseries(data, name, model, scenario, region, unit, groupby):
    ts = data.groupby([groupby, 'year'], as_index=False).sum()
    ts = pd.pivot_table(ts, columns='year', values='lvl').reset_index(
        drop=True)
    ts['model'] = model
    ts['scenario'] = scenario
    ts['region'] = region
    ts['variable'] = name
    ts['unit'] = unit
    return ts


def results_to_xlsx(model, scenario, database, shale_costs, carbon_costs):
    # Launch data base and load baseline
    mp = ixmp.Platform(dbprops=f'db/{database}', dbtype='HSQLDB')
    base = message_ix.Scenario(mp, model=model, scenario=scenario)
    folder = 'results/'

    all_ts = pd.DataFrame()

    # retrieve data from scenarios
    ##################################
    for s, c in [('none', 0)] + list(product(shale_costs, carbon_costs)):
        if s == 'none':
            scen = base
        else:
            scenario = f'{s}USDpMWh-{c}USDtCO2'
            scen = message_ix.Scenario(mp, model=model, scenario=scenario)

        scenario_ts = results_to_iamc(scen, model, scenario, 'South Africa', l_year=2050)
        all_ts = all_ts.append(scenario_ts, sort=True)

    if not os.path.exists(folder):
        os.makedirs(folder)

    all_ts.to_excel(folder + 'timeseries.xlsx', index=False)
    df = get_capacity_factor(all_ts)
    df.to_excel(folder + 'capacity_factors.xlsx', index=False)


def get_capacity_factor(ts_df):
    years = list(range(2020, 2060, 10))
    vars = ts_df['variable'].str.split('|', expand=True)
    for col in vars.columns:
        ts_df.insert(loc=col, column=str(col), value=vars[col])
    cap_df = ts_df[ts_df['0'].str.contains('Capacity')]
    act_df = ts_df[ts_df['0'].str.contains('Secondary Energy')]
    df = cap_df.merge(act_df, on=['1', '2', '3', 'model', 'scenario', 'region'], suffixes=['_cap', '_act'])
    for year in years:
        df.insert(4, f'{year}_flh', df[f'{year}_act'].multiply(8760).divide(df[f'{year}_cap']))
        df.insert(4, f'{year}_cap_fac', df[f'{year}_flh'].divide(8760))
    return df


def results_to_iamc(scen, model, scenario, region, l_year=2050):
    year = scen.set('year').astype(int)
    f_mod_year = scen.cat('year', 'firstmodelyear').astype(int)
    years = [year for year in year if (year >= f_mod_year) & (year <= int(l_year))]

    all_ts = pd.DataFrame()

    # retrieve data from scenarios
    ##################################
    # EMISSION DATA
    data = scen.var('EMISS', {'node': region, 'year': years}).drop(['type_tec', 'mrg'], axis=1)
    ts = create_timeseries(data, 'Emissions|GHG', model, scenario, region, 'MtCO2eq', 'node')
    all_ts = all_ts.append(ts, sort=True)

    # SECONDARY ENERGY DATA
    act_dic = {'Electricity|Coal': ['coal_adv', 'coal_ppl', 'igcc', 'coal_adv_ccs', 'igcc_ccs'],
               'Electricity|Coal|w/o CCS': ['coal_adv', 'coal_ppl', 'igcc'],
               'Electricity|Coal|w/ CCS': ['coal_adv_ccs', 'igcc_ccs'],
               'Electricity|Gas': ['gas_cc', 'gas_ct', 'gas_ppl', 'gas_cc_ccs'],
               'Electricity|Gas|w/o CCS': ['gas_cc', 'gas_ct', 'gas_ppl'],
               'Electricity|Gas|w/ CCS': ['gas_cc_ccs'],
               'Electricity|Oil': ['foil_ppl', 'loil_ppl'],
               'Electricity|Oil|w/o CCS': ['foil_ppl', 'loil_ppl'],
               'Electricity|Import': ['elec_imp'],
               'Electricity|Biomass': ['bio_istig'],
               'Electricity|Biomass|w/o CCS': ['bio_istig'],
               'Electricity|Wind': ['wind_ppl'],
               'Electricity|Solar': ['solar_th_ppl_base', 'solar_th_ppl', 'solar_pv_ppl'],
               'Electricity|Solar|CSP': ['solar_th_ppl_base', 'solar_th_ppl'],
               'Electricity|Solar|PV': ['solar_pv_ppl'],
               'Electricity|Hydro': ['hydro_ppl'],
               'Electricity|Nuclear': ['nuc_ppl'],
               'Liquids|Oil': ['ref_hil'],
               'Liquids|Coal': ['meth_coal', 'syn_liq', 'meth_coal_ccs', 'syn_liq_ccs'],
               'Liquids|Coal|w/o CCS': ['meth_coal', 'syn_liq'],
               'Liquids|Coal|w/ CCS': ['meth_coal_ccs', 'syn_liq_ccs'],
               'Liquids|Gas': ['meth_ng', 'meth_ng_ccs'],
               'Liquids|Gas|w/o CCS': ['meth_ng'],
               'Liquids|Gas|w/ CCS': ['meth_ng_ccs'],
               'Gases|Coal|w/o CCS': ['coal_gas'],
               'Gases|Bio|w/o CCS': ['gas_bio']
               }

    for k, t in act_dic.items():
        data = scen.var('ACT', {'node_loc': region, 'year_act': years, 'technology': t})
        data = data.rename(columns={'year_act': 'year'})
        ts = create_timeseries(data, f'Secondary Energy|{k}', model, scenario, region, 'GWa', 'node_loc')
        all_ts = all_ts.append(ts, sort=True)

        data = scen.var('CAP', {'node_loc': 'South Africa', 'year_act': years, 'technology': t})
        data = data.rename(columns={'year_act': 'year'})
        ts = create_timeseries(data, f'Capacity|{k}', model, scenario, region, 'GW', 'node_loc')
        all_ts = all_ts.append(ts, sort=True)

    # ENERGY RESOURCE USE DATA
    act_dic = {'shale_extr': 'shale_extr', 'coal_extr': 'coal_extr',
               'all_extr': ['shale_extr', 'coal_extr', 'gas_extr', 'oil_extr'],
               'all_imp': ['coal_imp', 'gas_imp', 'oil_imp', 'loil_imp', 'foil_imp', 'elec_imp'],
               'all_exp': ['coal_exp', 'gas_exp', 'oil_exp', 'loil_exp', 'foil_exp', 'elec_exp'],
               'renewable_energy': ['solar_th_ppl_base', 'solar_i', 'bio_extr', 'solar_rc', 'wind_ppl',
                                    'solar_pv_ppl', 'hydro_ppl', 'solar_th_ppl']}

    for k, t in act_dic.items():
        data = scen.var('ACT', {'node_loc': 'South Africa', 'year_act': years, 'technology': t})
        data = data.rename(columns={'year_act': 'year'})
        ts = create_timeseries(data, f'Activity|{k}', model, scenario, region, 'GWa', 'node_loc')
        all_ts = all_ts.append(ts, sort=True)

    return all_ts
