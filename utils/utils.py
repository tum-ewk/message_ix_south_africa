import pandas as pd

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

def load_data():
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'

    data['tax'] = [int(i.split(f'-')[1].replace('USDtCO2', '')) if len(i.split(f'-')) > 1 else 0 for i in data.scenario]
    data['cost'] = [round(float(i.split(f'-')[0].replace('USDpGJ', '')),1) if len(i.split(f'-')) > 1 else 'none' for i in
                    data.scenario]
    return data