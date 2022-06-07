# -*- coding: utf-8 -*-

r"""Implementation of the adjustable bi-fidelity Trid function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5

.. math::

    f_h(x_1, ..., x_{10}) = \sum^{10}_{i=1} (x_i - 1)^2 - \sum^{10}_{i=2} x_ix_{i-1}

.. math::

    f_l(x_1, ..., x_{10}) = \sum^{10}_{i=1} (x_i - a)^2 - (a - 0.65) \sum^{10}_{i=2} x_ix_{i-1}

where :math:`a \in [0, 1]` is the adjustable parameter
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


# u, l = [-d**2]*d, [d**2]*d
u_bound = [100]*10
l_bound = [-100]*10

x_opt = [10, 18, 24, 28, 30, 30, 28, 24, 18, 10]  # [i*(D+1-i) for i in range(1, D+1)]

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
    x_opt=x_opt,
)
