#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
mff_test.py: initial testing file for multifidelityfunctions package
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, integers, lists

from .multiFidelityFunction import row_vectorize, MultiFidelityFunction
from multifidelityfunctions import bohachevsky, booth, borehole, branin, currin, \
                                   forrester, hartmann, himmelblau, park91a, park91b, sixHumpCamelBack

from collections import namedtuple
ValueRange = namedtuple('ValueRange', ['min', 'max'])


def determinerange(values):
    """Determine the range of values in each dimension"""
    return ValueRange(np.min(values, axis=0), np.max(values, axis=0))


def rescale(values, *, range_in=None, range_out=ValueRange(0, 1), scale_only=False):
    """Perform a scale transformation of `values`: [range_in] --> [range_out]"""

    if range_in is None:
        range_in = determinerange(values)
    elif not isinstance(range_in, ValueRange):
        range_in = ValueRange(*range_in)

    if not isinstance(range_out, ValueRange):
        range_out = ValueRange(*range_out)

    scale_out = range_out.max - range_out.min
    scale_in = range_in.max - range_in.min

    if scale_only:
        scaled_values = (values / scale_in) * scale_out
    else:
        scaled_values = (values - range_in.min) / scale_in
        scaled_values = (scaled_values * scale_out) + range_out.min

    return scaled_values



@row_vectorize
def quadratic(xx):
    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = MultiFidelityFunction([-1e8], [1e8], [quadratic, quadratic], ['high', 'low'])

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
    for f, name in functions:
        X = rescale(np.array(x), range_in=ValueRange(0, 1),
                    range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))

        for fidelity in f.functions:
            _2d_array_input(fidelity, X.tolist())  # list input TODO: make separate test for @row_vectorize decorator instead
            _2d_array_input(fidelity, X)           # direct numpy input


# TESTS ------------------------------------------------------------------------


@given(rectangle_lists(n=2))
def test_2d_functions(x):
    functions = [
        (bohachevsky, 'bohachevsky'),
        (booth, 'booth'),
        (branin, 'branin'),
        (currin, 'currin'),
        (himmelblau, 'himmelblau'),
        (sixHumpCamelBack, 'sixhumpcamelback'),
    ]

    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=4))
def test_4d_functions(x):
    functions = [
        (park91a, 'park91a'),
        (park91b, 'park91b'),
    ]

    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=6))
def test_6d_functions(x):
    functions = [
        (hartmann, 'hartmann'),
    ]

    _iterate_over_functions(functions, x)


@given(rectangle_lists(n=8))
def test_8d_functions(x):
    functions = [
        (borehole, 'borehole'),
    ]

    _iterate_over_functions(functions, x)


@given(integers(min_value=1, max_value=100).flatmap(rectangle_lists))
def test_nd_functions(x):
    functions = [
        (simple_square, 'simple square'),
        (forrester, 'forrester'),
    ]

    _iterate_over_functions(functions, x)
