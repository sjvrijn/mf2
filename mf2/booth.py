# -*- coding: utf-8 -*-

"""Implementation of the bi-fidelity Booth function as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9

Function definitions:

.. math::

    f_h(x_1, x_2) = (x_1 + 2x_2 - 7)^2 + (2x_1 + x_2 - 5)^2

.. math::

    f_l(x_1, x_2) = f_h(0.4x_1, x_2) + 1.7x_1x_2 - x_1 + 2x_2
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


def booth_hf(xx):
    """
    BOOTH FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = (x1 + 2*x2 - 7)**2
    term2 = (2*x1 + x2 - 5)**2

    return term1 + term2


def booth_lf(xx):
    """
    BOOTH FUNCTION, LOWER FIDELITY CODE
    Calls: booth_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function booth_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = booth_hf(np.hstack([.4*x1.reshape(-1,1), x2.reshape(-1,1)]))
    term2 = 1.7*x1*x2 - x1 + 2*x2

    return term1 + term2


#: Lower bound for Booth function
l_bound = [-10, -10]
#: Upper bound for Booth function
u_bound = [ 10,  10]

x_opt = [1, 3]

#: 2D Booth function with fidelities 'high' and 'low'
booth = MultiFidelityFunction(
    "booth",
    u_bound, l_bound,
    [booth_hf, booth_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
