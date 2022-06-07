# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Branin function as defined in:

    Dong, H., Song, B., Wang, P. et al. Multi-fidelity information
    fusion based on prediction of kriging. Struct Multidisc Optim
    51, 1267–1280 (2015) doi:10.1007/s00158-014-1213-9

Function definitions:

.. math::

    f_b(x_1, x_2) = \Bigg(x_2 - (5.1\dfrac{x_1^2}{4\pi^2}) + \dfrac{5x_1}{\pi} -
                    6\Bigg)^2 + \Bigg(10\cos(x_1) (1 - \dfrac{1}{8\pi}\Bigg) + 10

.. math::

    f_h(x_1, x_2) = f_b(x_1, x_2) - 22.5x_2

.. math::

    f_l(x_1, x_2) = f_b(0.7x_1, 0.7x_2) - 15.75x_2 + 20(0.9 + x_1)^2 - 50
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


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
    term2 = 15.75*x2
    term3 = 20*(.9+x1)**2
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
