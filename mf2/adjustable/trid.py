# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Trid function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""


import numpy as np

from mf2.multi_fidelity_function import AdjustableMultiFidelityFunction


def trid_hf(xx):
    xx = np.atleast_2d(xx)

    temp1 = np.sum((xx - 1) ** 2, axis=1)
    temp2 = np.sum(xx[:,:-1] * xx[:,1:], axis=1)
    return temp1 - temp2

def adjustable_trid_lf(xx, a):
    xx = np.atleast_2d(xx)

    temp1 = np.sum((xx - a) ** 2, axis=1)
    temp2 = np.sum((a - 0.65) * xx[:, :-1] * xx[:, 1:] * np.arange(2, 11), axis=1)
    return temp1 - temp2


u_bound = [100]*10
l_bound = [-100]*10

docstring = """Factory method for adjustable Trid function using parameter value `a4`

    :param a4:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1].
    :return:    A MultiFidelityFunction instance
    """

trid = AdjustableMultiFidelityFunction(
    "Trid",
    u_bound, l_bound,
    [trid_hf],
    [adjustable_trid_lf],
    fidelity_names=['high', 'low'],
)
