import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set()


def plot_rainbow(df, groupby, y_ax_titel, figure_title='figure',
                 years=[2020, 2030, 2040, 2050], rel_NDC=False, lw=1.5):
    cmap = ['#000000', '#73BA9B', '#1d4504', '#740000', '#fe6b40', '#ffb366',
            '#FFC3A5', '#6f9c3d', '#a5c90f',
            '#000000', '#740000', '#fe6b40', '#ffb366', '#FFC3A5', '#1d4504',
            '#6f9c3d', '#a5c90f', '#73BA9B']
    colors = {}
    i = 0
    for gr in sorted(list(set(df[groupby]))):
        colors[gr] = cmap[i]
        i = i + 1
    if 'color' in df.columns:
        df = df.drop('color', axis=1)
    df['color'] = df[groupby].apply(lambda x: colors[x])

    fig, ax = plt.subplots(figsize=(8.4, 7))
    plt.style.use('seaborn-talk')
    ax.set_facecolor('white')
    fs = 24

    grouped = df.groupby(groupby)
    for key, group in grouped:
        # Plot shaded area per group
        fill = pd.DataFrame(index=years, columns=['min', 'max'])
        for yr in fill.index:
            fill.loc[yr, 'min'] = group[yr].min()
            fill.loc[yr, 'max'] = group[yr].max()
        ax.fill_between(years, fill['min'].tolist(), fill['max'].tolist(),
                        facecolor=colors[key], alpha=0.3)

        # Indicate baseline (no / least shale gas use)
        if groupby == 'tax':
            bl = group.loc[group.cost == df.cost.max()]
        elif groupby == 'cost':
            bl = group.loc[group.tax == df.tax.max()]
        ax.plot(years, bl[years].iloc[0].tolist(), color=colors[key], lw=lw)

        # Add Legend
        text = '{} {}'.format(int(group[groupby].mean()), '$/tCO2')
        height = float(bl[years[-1]])
        ax.text(years[-1]+2, height, text, fontsize=fs - 7, color=colors[key])

    # Add NDC
    if rel_NDC is False:
        ax.fill_between([2020, 2030, 2050],
                        [0.82 * 398, 0.82 * 398,  0.82 * 212],
                        [0.82 * 614, 0.82 * 614, 0.82 * 428],
                        alpha=0.2, color='gray')

    else:
        ax.fill_between([2020, 2030, 2050], [-25, -50, -82], [0, -23, -61],
                        alpha=0.2, color='gray')

    ax.set_ylabel(y_ax_titel, fontsize=fs - 2, color='dimgray')

    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(fs)
        label.set_color('dimgray')

    ax.grid(color='dimgray', linestyle='-', linewidth=1)

    plt.savefig(f'results//{figure_title}.png',
                bbox_inches='tight', dpi=100)
