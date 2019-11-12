import pandas as pd
from utils.plot.plot_heatmaps import plot_heatmaps


def plot_heatmap_comparison(years):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'

    data['tax'] = [int(i.split(f'-')[1].replace('USDtCO2', '')) if len(i.split(f'-')) > 1 else 0 for i in data.scenario]
    data['cost'] = [int(i.split(f'-')[0].replace('USDpMWh', '')) if len(i.split(f'-')) > 1 else 'none' for i in data.scenario]

    activity = data[~data.variable.str.contains('Capacity')].copy()

    plot_heatmaps(activity, years=years)
