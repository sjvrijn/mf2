# -*- coding: utf-8 -*-

"""Implementation of the bi-fidelity Six-hump Camel-back function
as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9
"""

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction


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

#: 2D Six-hump Camelback function with fidelities 'high' and 'low'
six_hump_camelback = MultiFidelityFunction(
    "six hump camelback",
    u_bound, l_bound,
    [six_hump_camelback_hf, six_hump_camelback_lf],
    fidelity_names=['high', 'low']
)
