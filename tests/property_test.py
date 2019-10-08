#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
property_test.py: testing file with property-based tests
for multifidelityfunctions package
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, integers, lists

from .utils import rescale, ValueRange
import multifidelityfunctions as mff


@mff.row_vectorize
def quadratic(xx):
    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = mff.MultiFidelityFunction('simple_square', [-1e8], [1e8], [quadratic, quadratic], ['high', 'low'])

# TEST HELPERS -----------------------------------------------------------------

def rectangle_lists(n):
    return lists(lists(floats(min_value=0, max_value=1),
                       min_size=n, max_size=n), min_size=1)


def _1d_array_input(func, x):
    y = func(x)

    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


def _2d_array_input(func, x):
    y = func(x)

    assert isinstance(y, np.ndarray)
    assert y.ndim == 1
    assert np.all(np.isfinite(y))


def _iterate_over_functions(functions, x):
    for f in functions:
        X = rescale(np.array(x), range_in=ValueRange(0, 1),
                    range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))

        for fidelity in f.functions:
            _2d_array_input(fidelity, X.tolist())  # list input TODO: make separate test for @row_vectorize decorator instead
            _2d_array_input(fidelity, X)           # direct numpy input


# TESTS ------------------------------------------------------------------------


@given(integers(min_value=1, max_value=100).flatmap(rectangle_lists))
def test_nd_functions(x):
    functions = [
        simple_square,
        mff.forrester,
    ]
    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=2))
def test_2d_functions(x):
    functions = [
        mff.bohachevsky,
        mff.booth,
        mff.branin,
        mff.currin,
        mff.himmelblau,
        mff.sixHumpCamelBack,
    ]
    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=4))
def test_4d_functions(x):
    functions = [
        mff.park91a,
        mff.park91b,
    ]
    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=6))
def test_6d_functions(x):
    functions = [
        mff.hartmann6,
    ]
    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=8))
def test_8d_functions(x):
    functions = [
        mff.borehole,
    ]
    _iterate_over_functions(functions, x)
