# -*- coding: utf-8 -*-

"""Implementation of the bi-fidelity Himmelblau function as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9

Function definitions:

.. math::

    f_h(x_1, x_2) = (x_1^2 + x_2 - 11)^2 + (x_2^2 + x_1 - 7)^2

.. math::

    f_l(x_1, x_2) = f_h(0.5x_1, 0.8x_2) + x_2^3 - (x_1+1)^2
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


def himmelblau_hf(xx):
    """
    HIMMELBLAU FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = (x1**2 + x2 - 11)**2
    term2 = (x2**2 + x1 - 7)**2

    return term1 + term2


def himmelblau_lf(xx):
    """
    HIMMELBLAU FUNCTION, LOWER FIDELITY CODE
    Calls: himmelblau_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function himmelblau_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = himmelblau_hf(np.hstack([0.5*x1.reshape(-1,1), 0.8*x2.reshape(-1,1)]))
    term2 = x2**3 - (x1 + 1)**2

    return term1 + term2


#: Lower bound for Himmelblau function
l_bound = [-4, -4]
#: Upper bound for Himmelblau function
u_bound = [ 4,  4]

x_opt = [3, 2]  # one of four optima

#: 2D Himmelblau function with fidelities 'high' and 'low'
himmelblau = MultiFidelityFunction(
    "himmelblau",
    u_bound, l_bound,
    [himmelblau_hf, himmelblau_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
