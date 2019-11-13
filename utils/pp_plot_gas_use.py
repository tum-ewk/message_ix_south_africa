import pandas as pd

from utils.plot.plot_facetgrid import plot_facet_grids
from utils.utils import get_plot_data, load_data


def plot_gas_use(s=None, c=None, order=None):
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

    synonyms = {'gas_use_power_sector': 'Power Sector', 'gas_use_industry': 'Industry',
                'gas_use_transformation': 'Residential and Others', 'gas_use_transport': 'Residential and Others',
                'gas_use_residential': 'Residential and Others'}

    col_dic = {'Power Sector': '#000000', 'Industry': '#A3CFD6', 'Residential and Others': '#b2b2b2',
               'Others': '#b2b2b2'}

    years = [2020, 2030, 2040, 2050]

    activity = get_plot_data(data, keyword='Input|Gas', synonyms=synonyms, col_dic=col_dic)
    activity[years] = activity[years] * 8760 * 3.6 * 10 ** -6 * 0.6
    plot_facet_grids(activity, y_title='Natural Gas Use [EJ]', figure_title='Gas_Use_EJ', col_dic=col_dic,
                     y_max=3.5, order=order)



