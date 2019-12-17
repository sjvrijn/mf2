#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Branin function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""




from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction
from mf2.branin import branin_base, l_bound, u_bound

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


_four_pi_square = 4*np.pi**2


def adjustable_branin_lf(xx, a1):
    xx = np.atleast_2d(xx)

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
