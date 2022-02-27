#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
property_test.py: testing file with property-based tests
for mf2 package
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


from itertools import chain

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import data, floats, integers, just, tuples
import pytest

from .utils import rescale, ValueRange
import mf2


def quadratic(xx):
    xx = np.atleast_2d(xx)

    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = mf2.MultiFidelityFunction('simple_square', [1e8], [-1e8], [quadratic, quadratic], ['high', 'low'])

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
def test_double_invert_idempotency(x):
    """Checks that applying invert() twice results in the same values"""
    orig = mf2.branin
    double_inverted = mf2.invert(mf2.invert(orig))
    assert np.allclose(orig.low(x), double_inverted.low(x))
    assert np.allclose(orig.high(x), double_inverted.high(x))


@given(ndim_array(n=2))
def test_invert_currin(x):
    """Test the optimum of the (inverted) Currin function"""
    currin = mf2.currin
    inverted_currin = mf2.invert(mf2.currin)
    x_opt = [0.21666666667, 0]
    y_opt = mf2.currin.high(x_opt)
    inverted_y_opt = y_opt * -1

    assert all(currin.high(x) < y_opt)
    assert all(inverted_currin.high(x) > inverted_y_opt)


@given(data())
@pytest.mark.parametrize("function", chain(
    mf2.bi_fidelity_functions,
    (f(0.5) for f in mf2.adjustable.bi_fidelity_functions),
))
def test_functions_run_without_error(function, data):
    x = data.draw(ndim_array(function.ndim))
    _test_single_function(function, x)


@pytest.mark.parametrize("function", mf2.bi_fidelity_functions)
def test_x_opt_is_optimum(function, n_cases=1_000):
    if function.x_opt is None:
        return
    if function.name == 'Currin':
        function = mf2.invert(function)

    x = rescale(np.random.rand(n_cases, function.ndim),
                range_in=ValueRange(0, 1),
                range_out=ValueRange(*function.bounds))
    y = function.high(x)

    y_opt = function.high(function.x_opt)
    assert np.all((y_opt - y) < 1e8)
