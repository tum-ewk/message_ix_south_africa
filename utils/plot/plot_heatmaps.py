import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use('seaborn-talk')


def convert_to_ej(a):
    a['value'] = a['value'] * 8760 * 3.6 * 10 ** (-6)  # GWa to GJ
    # a['value'] = a['value'] *10 # 10 year periods
    return a


def all_heatmap_plots(_plot_dic, name_dic, figure_title, lim_dic):
    fig = plt.figure(figsize=(3, 20))
    fig.subplots_adjust(hspace=0.4, wspace=0.2)

    sns.set(font_scale=1)
    for i in range(1, len(_plot_dic.keys()) + 1):
        _pf = _plot_dic[list(_plot_dic.keys())[i - 1]]
        title = name_dic[list(_plot_dic.keys())[i - 1]]
        vmin = lim_dic[list(_plot_dic.keys())[i - 1]][0]
        vmax = lim_dic[list(_plot_dic.keys())[i - 1]][1]

        ax = fig.add_subplot(6, 1, i)
        ax.set_facecolor('white')

        # Plot contour map colors
        sns.heatmap(_pf, cmap=plt.cm.viridis, xticklabels=4, yticklabels=2, vmin=vmin, vmax=vmax)
        cbar = ax.collections[0].colorbar
        ax.set_xlabel('Carbon Price  [$USD/CO_{2}$]')
        ax.set_ylabel('Shale Gas Cost [USD/GJ]')
        ax.set_title(f'{title}')
    plt.savefig(f'results\\{figure_title}.png', bbox_inches='tight', dpi=100)


def plot_heatmaps(_d, years):
    _d['value'] = _d[years].sum(axis=1)
    _d = _d[['variable', 'tax', 'cost', 'value']]

    # CO2 mitigation
    co2 = _d[_d['variable'] == 'Emissions|GHG'].copy()
    co2_nn = co2[(co2.cost == 'none')]['value']
    co2 = co2.assign(value = co2['value'].apply(lambda row: (row - co2_nn)/ co2_nn *100))
    co2['variable'] = 'Emissions|rel. Mitigation'
    _d = _d.append(co2, sort=True)

    # Fossil Energy Supply
    extr = _d[_d.variable == 'Activity|all_extr'][['cost', 'tax', 'value']].rename(columns={'value': 'value_extr'})
    imp = _d[_d.variable == 'Activity|all_imp'][['cost', 'tax', 'value']].rename(columns={'value': 'value_imp'})
    exp = _d[_d.variable == 'Activity|all_exp'][['cost', 'tax', 'value']].rename(columns={'value': 'value_exp'})
    _tpes = extr.merge(imp, how='outer', on=['cost', 'tax']).merge(exp, how='outer', on=['cost', 'tax'])

    _tpes = _tpes.assign(value=_tpes['value_extr'].add(_tpes['value_imp']).subtract(_tpes['value_exp']))
    _tpes['variable'] = 'TPES|fossil'
    _tpes = _tpes[_d.columns]
    _d = _d.append(_tpes, sort=True)

    _d = _d[_d.cost != 'none']

    # %% plot all data
    plot_dic = {}
    name_dic = {'Activity|shale_extr': '(a) Shale Gas Extraction [EJ]',
                'Activity|coal_extr': '(b) Coal Extraction [EJ]',
                'TPES|fossil': '(c) Fossil PE Supply [EJ]',
                'Activity|renewable_energy': '(d) RE Use [EJ]',
                'Emissions|rel. Mitigation': '(e) CO2 Mitigation [%]'}

    for name in name_dic.keys():
        _p = _d[_d.variable == name].copy()
        if name in ['Activity|shale_extr', 'Activity|coal_extr', 'TPES|fossil', 'Activity|renewable_energy']:
            _p = convert_to_ej(_p)

        pf = pd.pivot_table(_p, columns='tax', index='cost', values='value')
        if len(years) != 1 and name != 'Emissions|rel. Mitigation':
            pf = pf.multiply(10)
        plot_dic[name] = pf

    if len(years) == 1:
        figure_title = f'heat_maps_{years[0]}'
        lim_dic = {'Activity|shale_extr': [0, 6],
                   'Activity|coal_extr': [3, 8],
                   'TPES|fossil': [3, 8],
                   'Activity|renewable_energy': [0, 3],
                   'Emissions|rel. Mitigation': [-80, 0]}
    else:
        figure_title = f'heat_maps_cummulative'
        lim_dic = {'Activity|shale_extr': [0, 140],
                   'Activity|coal_extr': [140, 300],
                   'TPES|fossil': [140, 300],
                   'Activity|renewable_energy': [10, 70],
                   'Emissions|rel. Mitigation': [-60, 0]}
    all_heatmap_plots(plot_dic, name_dic, figure_title, lim_dic)
