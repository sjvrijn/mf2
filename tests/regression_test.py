#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
from pyprojroot import here
import pytest

from .utils import rescale, ValueRange
import mf2


_functions_to_test = (
    mf2.forrester,
    mf2.Forrester(ndim=2),
    mf2.Forrester(ndim=4),
    mf2.Forrester(ndim=6),
    mf2.Forrester(ndim=8),

    mf2.bohachevsky,
    mf2.booth,
    mf2.branin,
    mf2.currin,
    mf2.himmelblau,
    mf2.six_hump_camelback,
    mf2.park91a,
    mf2.park91b,
    mf2.hartmann6,
    mf2.borehole,

    mf2.adjustable.branin(0),
    mf2.adjustable.paciorek(0),
    mf2.adjustable.hartmann3(0),
    mf2.adjustable.trid(0),
)

@pytest.mark.parametrize("func", _functions_to_test)
def test_function_regression(func):

    data = rescale(np.load(here(f'tests/regression_files/input_{func.ndim}d.npy')),
                   range_in=ValueRange(0,1),
                   range_out=ValueRange(*func.bounds))

    for fid in func.fidelity_names:
        output = np.load(here(f'tests/regression_files/output_{func.ndim}d_{func.name}_{fid}.npy'))
        np.testing.assert_allclose(func[fid](data), output)
