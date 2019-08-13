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
def simple_square_high(xx):
    return np.sqrt(np.sum(xx**2, axis=1))


simple_square = MultiFidelityFunction([-1e8], [1e8], [simple_square_high], ['high'])


def _list_input(func, x):
    # x = [3, 4]
    y = func(x)

    # assert y[0] == 5
    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


def _double_list_input(func, x):
    # x = [[3, 4]]
    y = func(x)

    # assert y[0] == 5
    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


def _1d_array_input(func):
    x = np.array([3, 4])
    y = func(x)

    # assert y[0] == 5
    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


def _2d_array_input(func, x):
    # x = [[3, 4],
    #      [5, 12],
    #      [8, 15]]
    y = func(x)

    # assert y[0] == 5
    # assert y[1] == 13
    # assert y[2] == 17
    assert isinstance(y, np.ndarray)
    assert y.ndim == 1


# def test_simple_square():
#     _list_input(simple_square)
#     _double_list_input(simple_square)
#     _1d_array_input(simple_square)
#     _2d_array_input(simple_square)


@given(lists(lists(floats(min_value=0, max_value=1), min_size=2, max_size=2), min_size=1))
def test_2d_functions(x):
    functions = [
        (bohachevsky, 'bohachevsky'),
        (booth, 'booth'),
        (branin, 'branin'),
        (currin, 'currin'),
        (himmelblau, 'himmelblau'),
        (sixHumpCamelBack, 'sixhumpcamelback'),
    ]

    for f, name in functions:
        X = rescale(np.array(x), range_in=ValueRange(0,1), range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))
        # print(name)
        # _list_input(f.high)
        _double_list_input(f.high, X.tolist())
        # _1d_array_input(f.high)
        _2d_array_input(f.high, X)


@given(lists(lists(floats(min_value=0, max_value=1), min_size=4, max_size=4), min_size=1))
def test_4d_functions(x):
    pass


@given(lists(lists(floats(min_value=0, max_value=1), min_size=6, max_size=6), min_size=1))
def test_6d_functions(x):
    functions = [
        (hartmann, 'hartmann'),
    ]

    for f, name in functions:
        X = rescale(np.array(x), range_in=ValueRange(0,1), range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))
        # print(name)
        # _list_input(f.high)
        _double_list_input(f.high, X.tolist())
        # _1d_array_input(f.high)
        _2d_array_input(f.high, X)


@given(lists(lists(floats(min_value=0, max_value=1), min_size=8, max_size=8), min_size=1))
def test_8d_functions(x):
    functions = [
        (borehole, 'borehole'),
    ]

    for f, name in functions:
        X = rescale(np.array(x), range_in=ValueRange(0,1), range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))
        # print(name)
        # _list_input(f.high)
        _double_list_input(f.high, X.tolist())
        # _1d_array_input(f.high)
        _2d_array_input(f.high, X)


@given(integers(min_value=1, max_value=100).flatmap(lambda n: lists(lists(floats(min_value=0, max_value=1), min_size=n, max_size=n), min_size=1)))
def test_nd_functions(x):
    functions = [
        (simple_square, 'simple square'),
        (forrester, 'forrester'),
    ]

    for f, name in functions:
        X = rescale(np.array(x), range_in=ValueRange(0,1), range_out=ValueRange(np.array(f.l_bound), np.array(f.u_bound)))
        # print(name)
        # _list_input(f.high)
        _double_list_input(f.high, X.tolist())
        # _1d_array_input(f.high)
        _2d_array_input(f.high, X)
