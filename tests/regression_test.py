#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


import numpy as np
import pytest
import os
from hypothesis import given
from hypothesis.strategies import floats, integers, lists

from multifidelityfunctions.multiFidelityFunction import row_vectorize, MultiFidelityFunction
from multifidelityfunctions import bohachevsky, booth, borehole, branin, currin, \
                                   forrester, hartmann, himmelblau, park91a, park91b, sixHumpCamelBack


def test_hartmann6_regression():
    print(os.getcwd())
    data = np.load('tests/regression_files/input_6d.npy')
    output_high = np.load('tests/regression_files/output_hartmann6_high.npy')
    output_low = np.load('tests/regression_files/output_hartmann6_low.npy')

    np.testing.assert_allclose(hartmann.high(data), output_high)
    np.testing.assert_allclose(hartmann.low(data), output_low)



