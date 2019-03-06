import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-talk')


def convert_to_ej(a):
    a['value'] = a['value'] * 8.760 * 0.0036
    return a


def all_heatmap_plots(_plot_dic, name_dic):
    fig = plt.figure(figsize=(16, 8.4))
    fig.subplots_adjust(hspace=0.25, wspace=0.2)
    N = 6

    sns.set(font_scale=1)
    for i in range(1, len(_plot_dic.keys()) + 1):
        _pf = _plot_dic[list(_plot_dic.keys())[i - 1]]
        title = name_dic[list(_plot_dic.keys())[i - 1]]

        ax = fig.add_subplot(2, 3, i)
        ax.set_facecolor('white')

        # Plot contour map colors
        sns.heatmap(_pf, cmap=plt.cm.viridis, xticklabels=4, yticklabels=2)
        cbar = ax.collections[0].colorbar
        ax.set_xlabel('Carbon Price  [$USD/CO_{2}$]')
        ax.set_ylabel('Shale Gas Cost [USD/GJ]')
        ax.set_title(f'{title}')
    plt.savefig(f'results\\heat_maps.png', bbox_inches='tight',
                dpi=100)


def plot_heatmaps(_d, years):
    _d['value'] = _d[years].sum(axis=1)
    _d = _d[['variable', 'tax', 'cost', 'value']]

    # CO2 mitigation
    co2 = _d[_d['variable'] == 'Emissions|Total'].copy()
    co2_nn = co2[(co2.cost == 'none')]['value']
    co2['value'] = co2['value'].apply(lambda row: row - co2_nn)
    co2['value'] = co2['value'].apply(lambda row: row / co2_nn) * 100
    co2['variable'] = 'Emissions|rel. Mitigation'
    _d = _d.append(co2, sort=True)

    # Fossil Energy Supply
    extr = _d[_d.variable == 'Activity|all_extr'].value.values
    imp = _d[_d.variable == 'Activity|all_imp'].value.values
    exp = _d[_d.variable == 'Activity|all_exp'].value.values
    _tpes = _d[_d.variable == 'Activity|all_extr'].copy()
    _tpes['value'] = extr + imp - exp
    _tpes['variable'] = 'TPES|fossil'
    _d = _d.append(_tpes, sort=True)

    _d = _d[_d.cost != 'none']

    # %% plot all data
    plot_dic = {}
    name_dic = {'Activity|shale_extr':'(a) Shale Gas Extraction [EJ]',
                'TPES|fossil': '(b) Fossil PE Supply [EJ]',
                'Activity|coal_extr': '(c) Coal Extraction [EJ]',
                'Activity|renewable_energy': '(d) Renewable Energy Use [EJ]',
                'Emissions|rel. Mitigation': '(e) CO2 Mitigation [%]'}

    for name in name_dic.keys():
        _p = _d[_d.variable == name].copy()
        if name in ['Activity|shale_extr', 'Activity|coal_extr', 'TPES|fossil',
                    'Activity|renewable_energy']:
            _p = convert_to_ej(_p)

        _p['cost'] = [round(i / 8.760 / 3.6, 1) for i in _p['cost']]
        pf = pd.pivot_table(_p, columns='tax', index='cost', values='value')
        plot_dic[name] = pf

    all_heatmap_plots(plot_dic, name_dic)
