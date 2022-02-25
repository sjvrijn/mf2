# -*- coding: utf-8 -*-

"""Implementation of the bi-fidelity Bohachevsky function as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9
"""

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction


def bohachevsky_hf(xx):
    """
    BOHACHEVSKY FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = x1**2 + 2*x2**2
    term2 = 0.3*np.cos(3*np.pi*x1)
    term3 = 0.4*np.cos(4*np.pi*x2)

    return term1 - term2 - term3 + 0.7


def bohachevsky_lf(xx):
    """
    BOHACHEVSKY FUNCTION, LOWER FIDELITY CODE
    Calls: bohachevsky_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function bohachevsky_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = bohachevsky_hf(np.hstack([0.7*x1.reshape(-1,1), x2.reshape(-1,1)]))
    term2 = x1*x2 - 12

    return term1 + term2


#: Lower bound for Bohachevsky function
l_bound = [-5, -5]
#: Upper bound for Bohachevsky function
u_bound = [ 5,  5]

x_opt = [0,0]

#: 2D Bohachevsky function with fidelities 'high' and 'low'
bohachevsky = MultiFidelityFunction(
    "bohachevsky",
    u_bound, l_bound,
    [bohachevsky_hf, bohachevsky_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
