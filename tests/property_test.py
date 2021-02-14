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
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import floats, integers, just, tuples
import pytest

from .utils import rescale, ValueRange
import mf2


def quadratic(xx):
    xx = np.atleast_2d(xx)

    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = mf2.MultiFidelityFunction('simple_square', [-1e8], [1e8], [quadratic, quadratic], ['high', 'low'])

# TEST HELPERS -----------------------------------------------------------------
def ndim_array(n):
    return arrays(
        dtype=float,
        shape=tuples(integers(min_value=1, max_value=100), just(n)),
        elements=floats(0, 1),
    )


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
        _test_2d_array_input(fidelity, X.tolist())
        _test_2d_array_input(fidelity, X)  # direct numpy input


# TESTS ------------------------------------------------------------------------

def test_confirm_bifidelity_functions():
    fidelity_names = ['high', 'low']
    for f in mf2.bi_fidelity_functions:
        assert f.fidelity_names is not None
        assert len(f.fidelity_names) == len(f.functions) == 2
        for name in fidelity_names:
            assert name in f.fidelity_dict


@given(integers(min_value=1, max_value=100).flatmap(ndim_array))
@pytest.mark.parametrize("function", [
    simple_square,
    mf2.forrester,
])
def test_nd_functions(function, x):
    _test_single_function(function, x)


@given(integers(1, 100))
@pytest.mark.parametrize("factory", [
    mf2.Forrester,
])
def test_dimensionality_factory_valid_ndim(factory, ndim):
    func = factory(ndim)
    assert func.ndim == ndim


@given(integers(max_value=0))
@pytest.mark.parametrize("factory", [
    mf2.Forrester,
])
def test_dimensionality_factory_invalid_ndim(factory, ndim):
    with pytest.raises(ValueError):
        _ = factory(ndim)


@given(ndim_array(n=2))
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


@given(ndim_array(n=3))
@pytest.mark.parametrize("function", [
    mf2.adjustable.hartmann3(0.5),
])
def test_3d_functions(function, x):
    _test_single_function(function, x)


@given(ndim_array(n=4))
@pytest.mark.parametrize("function", [
    mf2.park91a,
    mf2.park91b,
])
def test_4d_functions(function, x):
    _test_single_function(function, x)


@given(ndim_array(n=6))
@pytest.mark.parametrize("function", [
    mf2.hartmann6,
])
def test_6d_functions(function, x):
    _test_single_function(function, x)


@given(ndim_array(n=8))
@pytest.mark.parametrize("function", [
    mf2.borehole,
])
def test_8d_functions(function, x):
    _test_single_function(function, x)


@given(ndim_array(n=10))
@pytest.mark.parametrize("function", [
    mf2.adjustable.trid(0.5),
])
def test_10d_functions(function, x):
    _test_single_function(function, x)
