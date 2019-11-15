import pandas as pd

from utils.plot.plot_facetgrid import plot_facet_grids
from utils.utils import get_plot_data, load_data


def plot_power_sector(s=None, c=None, order=None):
    data = load_data()
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
                     y_max=280, order=order)


