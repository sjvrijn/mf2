#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Filename.py: << A short summary docstring about this file >>
"""

from functools import partial

import numpy as np

from multifidelityfunctions.multiFidelityFunction import row_vectorize, MultiFidelityFunction
from multifidelityfunctions.branin import branin_base, l_bound, u_bound

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


_four_pi_square = 4*np.pi**2


@row_vectorize
def adjustable_branin_lf(xx, a1):

    x1, x2 = xx.T

    term1 = branin_base(xx)
    term2 = x2 - (5.1 * (x1**2 / _four_pi_square)) + ((5*x1) / np.pi) - 6

    return term1 - (a1+0.5) * term2**2


def branin(a1):

    return MultiFidelityFunction(
        f"adjustable Branin {a1}",
        u_bound, l_bound,
        [branin_base, partial(adjustable_branin_lf, a1=a1)],
        fidelity_names=['high', 'low'],
    )
