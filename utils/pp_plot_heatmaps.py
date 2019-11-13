import pandas as pd
from utils.plot.plot_heatmaps import plot_heatmaps
from utils.utils import load_data


def plot_heatmap_comparison(years):
    data = load_data()
    activity = data[~data.variable.str.contains('Capacity')].copy()
    bau_activity = activity[activity.cost == 'none']
    scen_activity = activity[activity.cost != 'none']
    scen_activity = scen_activity[scen_activity.cost <= 8.0] #!= max([i for i in activity.cost if type(i) == float])]
    activity = bau_activity.append(scen_activity, sort=True)
    plot_heatmaps(activity, years=years)
