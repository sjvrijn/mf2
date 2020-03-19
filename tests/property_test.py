#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
property_test.py: testing file with property-based tests
for mf2 package
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, integers, lists
import pytest

from .utils import rescale, ValueRange
import mf2


def quadratic(xx):
    xx = np.atleast_2d(xx)

    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = mf2.MultiFidelityFunction('simple_square', [-1e8], [1e8], [quadratic, quadratic], ['high', 'low'])

# TEST HELPERS -----------------------------------------------------------------

def rectangle_lists(n):
    return lists(lists(floats(min_value=0, max_value=1),
                       min_size=n, max_size=n), min_size=1)


def _test_1d_array_input(func, x):
    y = func(x)

    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


def _test_2d_array_input(func, x):
    y = func(x)

    assert isinstance(y, np.ndarray)
    assert y.ndim == 1
    assert np.all(np.isfinite(y))

    if len(x) > 1:
        assert np.allclose(func(x[0]), y[0])


def _test_single_function(f, x):
    X = rescale(np.array(x),
                range_in=ValueRange(0, 1),
                range_out=ValueRange(*f.bounds))
    for fidelity in f.functions:
        _test_2d_array_input(fidelity, X.tolist())  # list input TODO: make separate test for @row_vectorize decorator instead
        _test_2d_array_input(fidelity, X)  # direct numpy input


# TESTS ------------------------------------------------------------------------


@given(integers(min_value=1, max_value=100).flatmap(rectangle_lists))
@pytest.mark.parametrize("function", [
    simple_square,
    mf2.forrester,
])
def test_nd_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=2))
@pytest.mark.parametrize("function", [
    mf2.bohachevsky,
    mf2.booth,
    mf2.branin,
    mf2.currin,
    mf2.himmelblau,
    mf2.six_hump_camelback,
    mf2.adjustable.branin(0.5),
    mf2.adjustable.paciorek(0.5),
])
def test_2d_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=3))
@pytest.mark.parametrize("function", [
    mf2.adjustable.hartmann3(0.5),
])
def test_3d_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=4))
@pytest.mark.parametrize("function", [
    mf2.park91a,
    mf2.park91b,
])
def test_4d_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=6))
@pytest.mark.parametrize("function", [
    mf2.hartmann6,
])
def test_6d_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=8))
@pytest.mark.parametrize("function", [
    mf2.borehole,
])
def test_8d_functions(function, x):
    _test_single_function(function, x)


@given(rectangle_lists(n=10))
@pytest.mark.parametrize("function", [
    mf2.adjustable.trid(0.5),
])
def test_10d_functions(function, x):
    _test_single_function(function, x)
