import matplotlib.pyplot as plt

plt.style.use('seaborn-talk')


def plot_facet_grids(data, y_title, figure_title, col_dic, y_max=None):
    groups = data.groupby(['tax', 'cost'])
    s = list(set(data.cost))
    c = list(set(data.tax))

    cols = [i for i in data.columns if i not in ['variable', 'tax', 'cost']]

    fig = plt.figure(figsize=(14, 16))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    fig.set_facecolor('white')
    i = 1

    for key, group in groups:
        _pf = group[cols].copy()
        _o_tecs = _pf.loc[_pf.sum(axis=1) / _pf.sum(axis=1).sum() < 0.03,
                          :].index

        if len(_o_tecs) > 0:
            _other = _pf.loc[_o_tecs, :].sum(axis=0)
            _other.name = 'Other'
            _pf = _pf.drop(_o_tecs)
            _pf = _pf.append(_other, sort=True)

        ax = fig.add_subplot(len(s), len(c), i)
        ax.set_facecolor('white')

        if i != 9:
            plot_legend = False
        else:
            plot_legend = True

        _pf.T.plot(ax=ax, kind='bar', stacked=True, rot=0,
                   legend=plot_legend, color=[col_dic[i] for i in _pf.index],
                   width=0.8)
        # set title
        if i in [2, 3, 5, 6, 8, 9]:
            ax.axes.get_yaxis().set_ticks([])
        if i in [1, 2, 3, 4, 5, 6]:
            ax.get_xaxis().set_ticks([])
        if i in [1, 2, 3]:
            ax.set_title(f'{group.cost[0]}USD/GJ', fontsize=15)
        if i in [1, 4, 7]:
            ax.set_ylabel(f'{y_title} - {group.tax[0]} USD/CO2')
        if y_max:
            ax.set_ylim(bottom=0, top=y_max)
        i = i + 1

    plt.legend(loc='center left', bbox_to_anchor=(-2.2, -0.19), ncol=8)
    plt.savefig(f'results/{figure_title}.png', bbox_inches='tight')
