import pandas as pd
from utils.plot.plot_heatmaps import plot_heatmaps


def plot_heatmap_comparison(years=[2020, 2030, 2040, 2050]):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'

    activity = data[~data.variable.str.contains('Capacity')].copy()

    plot_heatmaps(activity, years=years)
