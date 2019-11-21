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


_functions_to_test = (
    mff.forrester,
    mff.Forrester(ndim=2),
    mff.Forrester(ndim=4),
    mff.Forrester(ndim=6),
    mff.Forrester(ndim=8),

    mff.bohachevsky,
    mff.booth,
    mff.branin,
    mff.currin,
    mff.himmelblau,
    mff.six_hump_camelback,
    mff.park91a,
    mff.park91b,
    mff.hartmann6,
    mff.borehole,

    mff.adjustable.branin(0),
    mff.adjustable.paciorek(0),
    mff.adjustable.hartmann3(0),
    mff.adjustable.trid(0),
)

@pytest.mark.parametrize("func", _functions_to_test)
def test_function_regression(func):

    data = rescale(np.load(Path(f'tests/regression_files/input_{func.ndim}d.npy')),
                   range_in=ValueRange(0,1),
                   range_out=ValueRange(*func.bounds))

    for fid in func.fidelity_names:
        output = np.load(Path(f'tests/regression_files/output_{func.ndim}d_{func.name}_{fid}.npy'))
        np.testing.assert_allclose(func[fid](data), output)
