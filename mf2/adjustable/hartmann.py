# -*- coding: utf-8 -*-

"""Implementation of the adjustable bi-fidelity Hartmann3 function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5
"""


from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction


# Some constant values
# Hartmann 3d
_alpha3 = np.array([1.0, 1.2, 3.0, 3.2])[:,np.newaxis]
_beta3 = np.array([
    [3.0, 10.0, 30.0],
    [0.1, 10.0, 35.0],
    [3.0, 10.0, 30.0],
    [0.1, 10.0, 35.0],
]).T[np.newaxis,:,:]
_P3 = np.array([
    [.3689, .1170, .2673],
    [.4699, .4387, .7470],
    [.1091, .8732, .5547],
    [.0381, .5743, .8828],
]).T[np.newaxis,:,:]


def hartmann3_hf(xx):
    xx = np.atleast_2d(xx)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P3) ** 2 * _beta3
    tmp2 = np.exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha3)

    return -tmp3.reshape((-1,))


def adjustable_hartmann3_lf(xx, a3):
    xx = np.atleast_2d(xx)

    factor = 3/4 * (a3+1)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - (_P3 * factor))
    tmp2 = tmp1 ** 2 * _beta3
    tmp3 = np.exp(-np.sum(tmp2, axis=1))
    tmp4 = tmp3.dot(_alpha3)

    return -tmp4.reshape((-1,))


u_bound = [1]*3
l_bound = [0]*3


def hartmann3(a3: float):
    """Factory method for adjustable Hartmann3 function using parameter value `a3`

    :param a3:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1]. High- and low-
                fidelity are identical for `a3=1/3`.
    :return:    A MultiFidelityFunction instance
    """

    return MultiFidelityFunction(
        f"adjustable Hartmann3 {a3}",
        u_bound, l_bound,
        [hartmann3_hf, partial(adjustable_hartmann3_lf, a3=a3)],
        fidelity_names=['high', 'low'],
    )

