# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Paciorek function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""


from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction


def paciorek_hf(xx):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    return np.sin(1/(x1*x2))


def adjustable_paciorek_lf(xx, a2):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    temp1 = paciorek_hf(xx)
    temp2 = 9 * a2**2
    temp3 = np.cos(1/(x1*x2))
    return temp1 - (temp2*temp3)


def paciorek(a2):
    """Factory method for adjustable Paciorek function using parameter value `a2`

    :param a2:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1]. High- and low-
                fidelity are identical for a1=-0.5.
    :return:    A MultiFidelityFunction instance
    """

    return MultiFidelityFunction(
        f"adjustable Paciorek {a2}",
        [1]*2, [0.3]*2,
        [paciorek_hf, partial(adjustable_paciorek_lf, a2=a2)],
        fidelity_names=['high', 'low'],
    )
