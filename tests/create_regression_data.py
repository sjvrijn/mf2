#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import multifidelityfunctions as mff
import numpy as np
from utils import rescale
from pathlib import Path


def create_and_store_input(ndim):
    fname = Path(f'regression_files/input_{ndim}d.npy')
    if not fname.exists():
        np.save(fname, np.random.rand(100,ndim))
        print(f"input {ndim}d created")


def create_and_store_output(ndim, func, fidelity):
    file_out = Path(f'regression_files/output_{ndim}d_{func.name}_{fidelity}.npy')
    if file_out.exists():
        return

    file_in = Path(f'regression_files/input_{ndim}d.npy')
    if not file_in.exists():
        create_and_store_input(ndim)

    x = rescale(np.load(file_in), range_in=(0,1),
                range_out=(np.array(func.l_bound), np.array(func.u_bound)))
    np.save(file_out, func[fidelity](x))
    print(f"output {ndim}d {func.name} created")


if __name__ == '__main__':
    for nd, func in [
        (1, mff.forrester),
        (2, mff.forrester),
        (4, mff.forrester),
        (6, mff.forrester),
        (8, mff.forrester),
        (2, mff.bohachevsky),
        (2, mff.booth),
        (2, mff.branin),
        (2, mff.adjustable_branin(0)),
        (2, mff.currin),
        (2, mff.himmelblau),
        (2, mff.adjustable_paciorek(0)),
        (2, mff.sixHumpCamelBack),
        (3, mff.adjustable_hartmann3(0)),
        (4, mff.park91a),
        (4, mff.park91b),
        (6, mff.hartmann6),
        (8, mff.borehole),
    ]:
        for fid in func.fidelity_names:
            create_and_store_output(nd, func, fid)
