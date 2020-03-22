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

    for func in mf2.bi_fidelity_functions:
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

    df = pd.DataFrame.from_records(records, columns=Record._fields)
    return df


save_location = Path('time_scaling.csv')
if not save_location.exists():
    df = create_and_store_time_scaling_data()
    df.to_csv(save_location, index=False)
else:
    df = pd.read_csv(save_location)


fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.8), constrained_layout=True)
plt.suptitle('Scalability of mf2-functions')
xticks = pd.unique(df['size'])
for ax, (fid, df_per_fid) in zip(axes, df.groupby('fidelity')):
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$N$')
    ax.set_ylabel('$t/t_0$')
    ax.set_title(f'{fid} fidelity')
    for ndim, df_per_dim in df_per_fid.groupby('ndim'):
        data = []
        for name, sub_df in df_per_dim.groupby('name'):
            data.append(sub_df['norm_time_per'].values)
        data = np.array(data)

        mean = np.mean(data, axis=0)
        label = f'{ndim}D'
        if data.shape[0] == 1:
            ax.plot(xticks, mean, label=label)
        else:
            min_max = np.abs(np.array([mean - np.min(data, axis=0),
                                       np.max(data, axis=0) - mean]))
            ax.errorbar(xticks, mean, min_max, label=label, capsize=4)


axes[0].legend(loc=0)
axes[1].legend(loc=0)
plt.savefig('scalability.pdf')
plt.savefig('scalability.png')
plt.show()
