# -*- coding: utf-8 -*-

r"""
forrester.py: Forrester function

This file contains the definition of an adapted version of the simple 1D
example function as presented in:

    Forrester Alexander I.J, Sóbester András and Keane Andy J "Multi-fidelity
    Optimization via Surrogate Modelling", Proceedings of the Royal Society A,
    vol. 463, http://doi.org/10.1098/rspa.2007.1900

Function definitions:

.. math::

    f_h(x) = (6x-2)^2 \sin(12x-4)

.. math::

    f_l(x) = A f_h(x) + B(x-0.5) + C

With :math:`A=0.5, B=10` and :math:`C=-5` as recommended parameters.

This version has been adapted to be multi-dimensional, input can be arbitrarily
many dimensions. Output value is calculated as the mean of the outcomes for all
separate dimensions.
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


def forrester_high(xx):
    xx = np.atleast_2d(xx)

    ndim = xx.shape[1]
    term1 = (6 * xx - 2) ** 2
    term2 = np.sin(12 * xx - 4)
    return np.sum(term1 * term2, axis=1) / ndim


def forrester_low(xx, *, A=0.5, B=10, C=-5):
    xx = np.atleast_2d(xx)

    ndim = xx.shape[1]
    term1 = A*forrester_high(xx)
    term2 = B*(xx - 0.5)
    term3 = C

    return term1 + (np.sum(term2, axis=1) / ndim) + term3


#: Lower bound for Forrester function
l_bound = [0]
#: Upper bound for Forrester function
u_bound = [1]

x_opt = [0.757248757841856]


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
        x_opt=np.repeat(x_opt, ndim),
    )


#: 1D Forrester function with fidelities 'high' and 'low'
forrester = Forrester(ndim=1)

#: 1D Forrester function with single fidelity 'high'
forrester_sf = MultiFidelityFunction(
    "forrester single fidelity",
    u_bound=u_bound, l_bound=l_bound,
    functions=[forrester_high],
    fidelity_names=['high'],
    x_opt=x_opt,
)
