#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
import pytest

from .utils import rescale, ValueRange
import mf2


_functions_to_test = (
    mf2.forrester,
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


def idfn(func):
    return f"{func.ndim}D-{func.name}"


@pytest.mark.parametrize("func", _functions_to_test, ids=idfn)
def test_function_regression(num_regression, func):
    np.random.seed(20160501)
    data_in = rescale(np.random.rand(100, func.ndim),
                      range_in=ValueRange(0,1),
                      range_out=ValueRange(*func.bounds))

    num_regression.check({
        fid: func[fid](data_in) for fid in func.fidelity_names
    })


def test_xopt_regression(num_regression):
    num_regression.check({
        func.name: func.high(func.x_opt)
        for func in _functions_to_test
        if func.x_opt is not None
    })
