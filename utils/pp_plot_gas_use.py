import pandas as pd

from utils.plot.plot_facetgrid import plot_facet_grids


def plot_gas_use(s=None, c=None, order=None):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'

    data['tax'] = [int(i.split(f'-')[1].replace('USDtCO2', '')) if len(i.split(f'-')) > 1 else 0 for i in data.scenario]
    data['cost'] = [int(i.split(f'-')[0].replace('USDpMWh', '')) if len(i.split(f'-')) > 1 else 'none' for i in
                    data.scenario]

    data = data[data.cost != 'none']

    if s is None:
        all_cost = sorted(list(set(data.cost)))
        s = [min(all_cost), all_cost[int((len(all_cost) - 1) / 2)], max(all_cost)]

    if c is None:
        all_cost = sorted(list(set(data.tax)))
        c = [min(all_cost), all_cost[int((len(all_cost) - 1) / 2)], max(all_cost)]

    data = data[data.cost.isin(s)]
    data = data[data.tax.isin(c)]

    synonyms = {'Solar': 'Renewable', 'Hydro': 'Renewable', 'Wind': 'Renewable', 'Biomass': 'Renewable',
                'Import': 'Others', 'Oil': 'Others'}

    col_dic = {'Coal|w/o CCS': '#000000', 'Coal|w/ CCS': '#918F88',
               'Gas|w/o CCS': '#A3CFD6', 'Gas|w/ CCS': '#D3EAED',
               'Renewable': '#4EB378', 'Nuclear': '#724ac1', 'Others': '#b2b2b2'}

    years = [2020, 2030, 2040, 2050]
    activity = get_plot_data(data, keyword='Secondary Energy|Electricity', synonyms=synonyms, col_dic=col_dic)
    activity[years] = activity[years] * 8.760
    plot_facet_grids(activity, y_title='PPL Activity [TWh]', figure_title='Power_Activity_TWh', col_dic=col_dic,
                     y_max=880, order=order)

    capacity = get_plot_data(data, keyword='Capacity|Electricity', synonyms=synonyms, col_dic=col_dic)
    plot_facet_grids(capacity, y_title='PPL Capacity [GW]', figure_title='Power_Capacity_GW', col_dic=col_dic,
                     y_max=350, order=order)


def get_plot_data(data, keyword, synonyms, col_dic):
    _df = data[
        (data.variable.str.contains(keyword.split('|')[0])) & (data.variable.str.contains(keyword.split('|')[1]))]
    _df = _df.assign(variable=[i for i in _df['variable'].str.replace(keyword, '').str.strip('|')])
    for tec, syn in synonyms.items():
        _df.loc[_df['variable'] == tec, 'variable'] = [syn for _ in _df[_df.variable == tec].variable]
    _df = _df.groupby(by=['cost', 'tax', 'variable'], ).sum().reset_index()
    _df = _df.set_index('variable', drop=True)
    _df = _df[_df.index.isin(col_dic.keys())]
    return _df
