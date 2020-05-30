from collections import namedtuple
from pathlib import Path
from timeit import Timer

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import mf2


def create_and_store_time_scaling_data():
    Record = namedtuple('Record', 'ndim name size fidelity number time_per norm_time_per')
    records = []

    bi_fidelity_functions = [
        *mf2.bi_fidelity_functions,
        *[func(0.5) for func in mf2.adjustable.bi_fidelity_functions]
    ]

    for func in bi_fidelity_functions:
        print(func.name)

        base_times = {'high': None, 'low': None}
        for size in [10**i for i in range(7)]:
            print(size, end=' ', flush=True)
            for fid in ('high', 'low'):
                t = Timer(
                    stmt=f'func.{fid}(X)',
                    setup=f'X = np.random.rand({size}, {func.ndim})',
                    globals={'np': np, 'func': func},
                )
                num, time = t.autorange()
                time_per = time/num
                if base_times[fid] is None:
                    base_times[fid] = time_per
                    norm_time_per = 1
                else:
                    norm_time_per = (time/num) / base_times[fid]
                records.append(Record(func.ndim, func.name, size, fid, num, time_per, norm_time_per))
        print()

    return pd.DataFrame.from_records(records, columns=Record._fields)


def plot_mf2_scalability(df):

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.8), constrained_layout=True)
    plt.suptitle('Scalability of mf2-functions')
    xticks = pd.unique(df['size'])
    y_lim = 10**(np.log10(df['norm_time_per'].max()) + 1)
    x_lim = 10**(np.log10(df['size'].max()) + 1)
    for ax, (fid, df_per_fid) in zip(axes, df.groupby('fidelity')):
        ax.grid(linestyle='--', linewidth=1, alpha=.5)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('$N$')
        ax.set_ylabel('$t/t_0$')
        ax.set_title(f'{fid} fidelity')
        ax.set_xlim(right=x_lim)
        ax.set_ylim(top=y_lim)
        for ndim, df_per_dim in df_per_fid.groupby('ndim'):
            data, names = [], []
            for name, sub_df in df_per_dim.groupby('name'):
                data.append(sub_df['norm_time_per'].values)
                names.append(name)
            data = np.array(data)

            mean = np.mean(data, axis=0)
            if data.shape[0] == 1:
                label = names[0].title()
                if 'Adjustable' in label:
                    label = label[len('Adjustable'):-len('0.5')].title()
                ax.plot(xticks, mean, label=label)
            else:
                label = f'Mean of {len(names)} {ndim}D functions'
                min_max = np.abs(np.array([mean - np.min(data, axis=0),
                                           np.max(data, axis=0) - mean]))
                ax.errorbar(xticks, mean, min_max, label=label, capsize=4)

    axes[0].legend(loc=0)
    axes[1].legend(loc=0)
    plt.savefig('scalability.pdf')
    plt.savefig('scalability.png')
    plt.show()


def plot_scalability_comparison(df1, df2, name1, name2):

    names1, names2 = pd.unique(df1['name']), pd.unique(df2['name'])
    df1 = df1.loc[df1['name'].isin(names2)]
    df2 = df2.loc[df2['name'].isin(names1)]

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.8), constrained_layout=True)
    plt.suptitle(f'{name1} vs {name2}')
    xticks = pd.unique(df1['size'])

    df = pd.concat([df1, df2])
    y_lim = 10**(np.log10(df['norm_time_per'].max()) + 1)
    x_lim = 10**(np.log10(df['size'].max()) + 1)

    for ax, (fid, df_per_fid1), (_, df_per_fid2) in zip(axes, df1.groupby('fidelity'), df2.groupby('fidelity')):
        ax.grid(linestyle='--', linewidth=1, alpha=.5)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('$N$')
        ax.set_ylabel('$t/t_0$')
        ax.set_title(f'{fid} fidelity')
        ax.set_xlim(right=x_lim)
        ax.set_ylim(top=y_lim)
        for (ndim, df_per_dim1), (_, df_per_dim2) in zip(df_per_fid1.groupby('ndim'), df_per_fid2.groupby('ndim')):
            data1, data2, names = [], [], []
            for (name, sub_df1), (_, sub_df2) in zip(df_per_dim1.groupby('name'), df_per_dim2.groupby('name')):
                data1.append(sub_df1['norm_time_per'].values)
                data2.append(sub_df2['norm_time_per'].values)
                names.append(name)
            data1, data2 = np.array(data1), np.array(data2)

            for data, name, linestyle in zip([data1, data2], [name1, name2], ['-', '--']):
                mean = np.mean(data, axis=0)
                if data.shape[0] == 1:
                    label = names[0].title()
                    if 'Adjustable' in label:
                        label = label[len('Adjustable'):-len('0.5')].title()
                    ax.plot(xticks, mean, linestyle, label=f'{name}: {label}')
                else:
                    label = f'{name}: Mean of {len(names)} {ndim}D functions'
                    min_max = np.abs(np.array([mean - np.min(data, axis=0),
                                               np.max(data, axis=0) - mean]))
                    ax.errorbar(xticks, mean, min_max, fmt=linestyle, label=label, capsize=4)


    axes[0].legend(loc=0)
    axes[1].legend(loc=0)
    plt.savefig('scalability_comparison.pdf')
    plt.savefig('scalability_comparison.png')
    plt.show()


def main():
    np.random.seed(20160501)
    save_location = Path('time_scaling.csv')
    if not save_location.exists():
        df = create_and_store_time_scaling_data()
        df.to_csv(save_location, index=False)
    else:
        df = pd.read_csv(save_location)
    plot_mf2_scalability(df)

    matlab_save_location = Path('time_scaling_matlab.csv')
    matlab_df = pd.read_csv(matlab_save_location)
    plot_scalability_comparison(df, matlab_df, 'mf2 (Python)', 'S&B (Matlab)')


if __name__ == '__main__':
    main()
