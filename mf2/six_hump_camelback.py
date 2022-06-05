# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Six-hump Camel-back function
as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9

Function definitions:

.. math::

    f_h(x_1, x_2) = 4x_1^2 - 2.1x_1^4 + \dfrac{x_1^6}{3} + x_1x_2 - 4x_2^2 + 4x_2^4

.. math::

    f_l(x_1, x_2) = f_h(0.7x_1, 0.7x_2) + x_1x_2 - 15
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


def six_hump_camelback_hf(xx):
    """
    SIX-HUMP CAMEL-BACK FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    x1sq, x2sq = x1*x1, x2*x2

    term1 = (4 - 2.1*x1sq + (x1sq*x1sq)/3) * x1sq
    term2 = x1*x2
    term3 = (-4 + 4*x2sq) * x2sq

    return term1 + term2 + term3


def six_hump_camelback_lf(xx):
    """
    SIX-HUMP CAMEL-BACK FUNCTION, LOWER FIDELITY CODE
    Calls: sixHumpCamelBack_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function sixHumpCamelBack_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = six_hump_camelback_hf(np.hstack([0.7 * x1.reshape(-1, 1), 0.7 * x2.reshape(-1, 1)]))
    term2 = x1*x2 - 15

    return term1 + term2


#: Lower bound for Six-hump Camelback function
l_bound = [-2, -2]
#: upper bound for Six-hump Camelback function
u_bound = [ 2,  2]

x_opt = [0.0898, -0.7126]

#: 2D Six-hump Camelback function with fidelities 'high' and 'low'
six_hump_camelback = MultiFidelityFunction(
    "six hump camelback",
    u_bound, l_bound,
    [six_hump_camelback_hf, six_hump_camelback_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
