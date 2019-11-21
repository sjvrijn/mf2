#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
import pytest
from pathlib import Path

from .utils import rescale, ValueRange
import multifidelityfunctions as mff


@pytest.mark.parametrize("ndim,func", [
    (1, mff.forrester),
    (2, mff.forrester),
    (4, mff.forrester),
    (6, mff.forrester),
    (8, mff.forrester),

    (2, mff.bohachevsky),
    (2, mff.booth),
    (2, mff.branin),
    (2, mff.currin),
    (2, mff.himmelblau),
    (2, mff.six_hump_camelback),
    (4, mff.park91a),
    (4, mff.park91b),
    (6, mff.hartmann6),
    (8, mff.borehole),

    (2, mff.adjustable.branin(0)),
    (2, mff.adjustable.paciorek(0)),
    (3, mff.adjustable.hartmann3(0)),
    (10, mff.adjustable.trid(0)),
])
def test_function_regression(ndim, func):

    data = rescale(np.load(Path(f'tests/regression_files/input_{ndim}d.npy')),
                   range_in=ValueRange(0,1),
                   range_out=ValueRange(*func.bounds))

    for fid in func.fidelity_names:
        output = np.load(Path(f'tests/regression_files/output_{ndim}d_{func.name}_{fid}.npy'))
        np.testing.assert_allclose(func[fid](data), output)
