# -*- coding: utf-8 -*-

"""
hartmann.py: contains the Hartmann 3d and 6d function

As defined in
 [3d] "Some Considerations Regarding the Use of Multi-fidelity Kriging in the
      Construction of Surrogate Models" by David J.J. Toal (2015)
 [6d] "Remarks on multi-fidelity surrogates" by Chanyoung Park, Raphael T. Haftka 
      and Nam H. Kim (2016)
"""

from functools import partial

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize

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

# Hartmann 6d
_alpha6_low = np.array([0.5, 0.5, 2.0, 4.0])[:,np.newaxis]
_alpha6_high = np.array([1.0, 1.2, 3.0, 3.2])[:, np.newaxis]
_A6 = np.array([
    [10.00,  3.0, 17.00,  3.5,  1.7,  8],
    [ 0.05, 10.0, 17.00,  0.1,  8.0, 14],
    [ 3.00,  3.5,  1.70, 10.0, 17.0,  8],
    [17.00,  8.0,  0.05, 10.0,  0.1, 14],
]).T[np.newaxis,:,:]
_P6 = np.array([
    [.1312, .1696, .5569, .0124, .8283, .5886],
    [.2329, .4135, .8307, .3736, .1004, .9991],
    [.2348, .1451, .3522, .2883, .3047, .6650],
    [.4047, .8828, .8732, .5743, .1091, .0381],
]).T[np.newaxis,:,:]
_four_nine_exp = np.exp(-4 / 9)


@row_vectorize
def hartmann3_hf(xx):

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P3) ** 2 * _beta3
    tmp2 = np.exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha3)

    return -tmp3.reshape((-1,))


@row_vectorize
def adjustable_hartmann3_lf(xx, a3):

    factor = 3/4 * (a3+1)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - (_P3 * factor))
    tmp2 = tmp1 ** 2 * _beta3
    tmp3 = np.exp(-np.sum(tmp2, axis=1))
    tmp4 = tmp3.dot(_alpha3)

    return -tmp4.reshape((-1,))


def adjustable_hartmann3(a3):

    return MultiFidelityFunction(
        f"adjustable Hartmann3 {a3}",
        [1] * 3, [0] * 3,
        [hartmann3_hf, partial(adjustable_hartmann3_lf, a3=a3)],
        fidelity_names=['high', 'low'],
    )


@row_vectorize
def hartmann6_hf(xx):

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P6) ** 2 * _A6
    tmp2 = np.exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha6_high) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


@row_vectorize
def hartmann6_lf(xx):

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P6) ** 2 * _A6
    tmp2 = f_exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha6_low) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


def f_exp(xx):

    return (_four_nine_exp + (_four_nine_exp * (xx + 4)/9)) ** 9


hartmann6 = MultiFidelityFunction(
    "Hartmann 6",
    [1] * 6, [0.1] * 6,
    [hartmann6_hf, hartmann6_lf],
    fidelity_names=['high', 'low']
)
