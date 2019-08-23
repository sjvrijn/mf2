#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np

from .multiFidelityFunction import row_vectorize, MultiFidelityFunction

"""
FR.py: Forrester function

This file contains the definition of an adapted version of the simple 1D
example function as presented in the paper(s) by Forrester et al.

This version has been adapted in the following ways:
 - Inverted, the optimum is a maximum, not a minimum
 - Translated, the (1D) output values have been translated upwards to always
   be positive, i.e. [~0, ~22]
 - Multi-dimensional, input can be arbitrarily many dimensions. Output value
   is calculated as the weighted sum of each separable dimension.
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


l_bound = [0]
u_bound = [1]

@row_vectorize
def forrester_high(X):
    ndim = X.shape[1]
    term1 = (6*X - 2)**2
    term2 = np.sin(12*X - 4)
    return np.sum(22 - (term1 * term2 + 6.03), axis=1) / ndim


@row_vectorize
def forrester_low(X):
    ndim = X.shape[1]
    term1 = 0.5*forrester_high(X)
    term2 = 10*(X - 0.5) - 5

    return term1 - (np.sum(term2, axis=1) / ndim)


forrester = MultiFidelityFunction(
    "forrester",
    u_bound=u_bound, l_bound=l_bound,
    functions=[forrester_high, forrester_low],
    fidelity_names=['high', 'low'],
)

forrester_sf = MultiFidelityFunction(
    "forrester single fidelity",
    u_bound=u_bound, l_bound=l_bound,
    functions=[forrester_high],
    fidelity_names=['high'],
)
