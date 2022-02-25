# -*- coding: utf-8 -*-

"""Implementation of the bi-fidelity Branin function as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9
"""

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction


_four_pi_square = 4*np.pi**2
_eight_pi = 8*np.pi


def branin_base(xx):
    """
    BRANIN FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = x2 - (5.1 * (x1**2 / _four_pi_square)) + ((5*x1) / np.pi) - 6
    term2 = (10 * np.cos(x1)) * (1 - (1/_eight_pi))

    return term1**2 + term2 + 10


def branin_hf(xx):
    """
    BRANIN FUNCTION, HIGH FIDELITY CODE
    Calls: branin_base
    This function, from Dong et al. (2015), is used as the "high-accuracy code"
    version of the function based on the 'traditional' branin function.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    _, x2 = xx.T
    return branin_base(xx) - 22.5*x2


def branin_lf(xx):
    """
    BRANIN FUNCTION, LOWER FIDELITY CODE
    Calls: branin_base
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function branin_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = branin_base(np.hstack([0.7*x1.reshape(-1,1), 0.7*x2.reshape(-1,1)]))
    term2 = 1.575*x2  # 15.75
    term3 = 2*(.9+x1**2)
    term4 = 50

    return term1 - term2 + term3 - term4


#: Lower bound for Branin function
l_bound = [-5,  0]
#: Upper bound for Branin function
u_bound = [10, 15]

x_opt = [-3.786088705282203, 15]

#: 2D Branin function with fidelities 'high' and 'low'
branin = MultiFidelityFunction(
    "branin",
    u_bound, l_bound,
    [branin_hf, branin_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
