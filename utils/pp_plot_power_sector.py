import pandas as pd
from utils.plot.plot_facetgrid import plot_facet_grids


def plot_power_sector(s=None, c=None):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'
    
    data = data[data.cost != 'none']

    if s is None:
        all_cost = sorted(list(set(data.cost)))
        s = [min(all_cost), all_cost[int((len(all_cost) - 1) / 2)],
             max(all_cost)]

    if c is None:
        all_cost = sorted(list(set(data.tax)))
        c = [min(all_cost), all_cost[int((len(all_cost) - 1) / 2)],
             max(all_cost)]

    data = data[data.cost.isin(s)]
    data = data[data.tax.isin(c)]
    data.index = [i.split('|')[1] for i in data['variable']]

    col_dic = {'Gas wo ccs': '#A3CFD6',
               'Gas ccs': '#D3EAED',
               'Coal wo ccs': '#000000',
               'Coal ccs': '#918F88',
               'Other ppls': '#b2b2b2',
               'Renewable': '#4EB378',
               'Nuclear': '#724ac1',
               'Other': '#b2b2b2',
               }

    activity = data[data.variable.str.contains('Activity')]
    activity = activity[activity.index.isin(list(col_dic.keys()))]
    plot_facet_grids(activity, y_title='PPL Activity [GWa]',
                     figure_title='Power_Activity_GWa',
                     col_dic=col_dic, y_max=110)

    capacity = data[data.variable.str.contains('Capacity')]
    capacity = capacity[capacity.index.isin(list(col_dic.keys()))]
    plot_facet_grids(capacity, y_title='PPL Capacity [GW]',
                     figure_title='Power_Capacity_GW',
                     col_dic=col_dic, y_max=350)
