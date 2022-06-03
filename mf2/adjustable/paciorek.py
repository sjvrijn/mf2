# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Paciorek function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""


import numpy as np

from mf2.multi_fidelity_function import AdjustableMultiFidelityFunction


def paciorek_hf(xx):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    return np.sin(1/(x1*x2))


def adjustable_paciorek_lf(xx, a):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    temp1 = paciorek_hf(xx)
    temp2 = 9 * a ** 2
    temp3 = np.cos(1/(x1*x2))
    return temp1 - (temp2*temp3)


u_bound = [1]*2
l_bound = [0.3]*2

docstring = """Factory method for adjustable Paciorek function using parameter value `a2`

    :param a2:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1]. High- and low-
                fidelity are identical for `a2=0.0`.
    :return:    A MultiFidelityFunction instance
    """

paciorek = AdjustableMultiFidelityFunction(
    "Paciorek",
    u_bound, l_bound,
    [paciorek_hf],
    [adjustable_paciorek_lf],
    fidelity_names=['high', 'low'],
)
