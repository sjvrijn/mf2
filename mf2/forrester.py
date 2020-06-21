# -*- coding: utf-8 -*-

"""
forrester.py: Forrester function

This file contains the definition of an adapted version of the simple 1D
example function as presented in:

    Forrester Alexander I.J, Sóbester András and Keane Andy J "Multi-fidelity
    Optimization via Surrogate Modelling", Proceedings of the Royal Society A,
    vol. 463, http://doi.org/10.1098/rspa.2007.1900

This version has been adapted to be multi-dimensional, input can be arbitrarily
many dimensions. Output value is calculated as the mean of the outcomes for all
separate dimensions.
"""

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction


def forrester_high(X):
    X = np.atleast_2d(X)

    ndim = X.shape[1]
    term1 = (6*X - 2)**2
    term2 = np.sin(12*X - 4)
    return np.sum(term1 * term2, axis=1) / ndim


def forrester_low(X, *, A=0.5, B=10, C=-5):
    X = np.atleast_2d(X)

    ndim = X.shape[1]
    term1 = A*forrester_high(X)
    term2 = B*(X - 0.5)
    term3 = C

    return term1 + (np.sum(term2, axis=1) / ndim) + term3


#: Lower bound for Forrester function
l_bound = [0]
#: Upper bound for Forrester function
u_bound = [1]


def Forrester(ndim: int):
    """Factory method for `ndim`-dimensional multi-fidelity Forrester function

    :param ndim: Desired dimensionality
    :return:     :class:`~mf2.multiFidelityFunction.MultiFidelityFunction`
                 instance with bounds of appropriate length
    """
    if ndim < 1:
        raise ValueError(f"ndim must be at least 1, not {ndim}")

    return MultiFidelityFunction(
        "forrester",
        u_bound=np.repeat(u_bound, ndim),
        l_bound=np.repeat(l_bound, ndim),
        functions=[forrester_high, forrester_low],
        fidelity_names=['high', 'low'],
    )


#: 1D Forrester function with fidelities 'high' and 'low'
forrester = Forrester(ndim=1)

#: 1D Forrester function with single fidelity 'high'
forrester_sf = MultiFidelityFunction(
    "forrester single fidelity",
    u_bound=u_bound, l_bound=l_bound,
    functions=[forrester_high],
    fidelity_names=['high'],
)
