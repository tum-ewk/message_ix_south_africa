import pandas as pd
import matplotlib.pyplot as plt
from utils.plot.plot_rainbow import plot_rainbow

plt.style.use('seaborn-talk')


def plot_emissions(c=None):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'
    if c:
        data = data[data.tax.isin(c)]

    base = data.loc[(data.tax == 0) & (data.cost == 'none')].copy()
    scenarios = data.loc[(data.cost != 'none')].copy()

    # Shale gas costs from MUSD/GWa to USD/GJ
    scenarios.loc[:, 'cost'] = [round(i / 8.76 / 3.6, 1) for i in
                                scenarios.loc[:, 'cost']]
    col = [i for i in data.columns if
           i not in ['cost', 'tax', 'color', 'variable']]

    # TOTAL EMISSIONS in the shale gas and the no-shale gas scenarios
    df = scenarios.loc[
        scenarios.variable == 'Emissions|Total'].copy().reset_index(
        drop=True).drop('variable', axis=1).dropna()
    plot_rainbow(df, 'tax', 'Total Emissions [$MtCO_{2e}$]', 'Total Emissions',
                 [2020, 2030, 2040, 2050])

    # EMISSION REDUCTION in the no-shale-gas scenarios
    df[col] = df[col].subtract(base[col].values[0], axis=1).copy()
    rel_mit = df.copy()
    rel_mit[col] = rel_mit[col].divide(base[col].values[0], axis=1) * 100

    rel_mit_ng = rel_mit[rel_mit.cost == rel_mit.cost.max()]
    plot_rainbow(rel_mit_ng, 'tax', 'Emission Reduction [%]',
                 'Emission Reduction', [2020, 2030, 2040, 2050], rel_NDC=True,
                 lw=2.5)
