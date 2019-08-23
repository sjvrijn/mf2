#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize
"""
Hartmann.py: contains the Hartmann 6d function

As defined in "Remarks on multi-fidelity surrogates" by Chanyoung Park, 
Raphael T. Haftka and Nam H. Kim (2016)

"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


# Some constant values
_A = np.array([
    [10.00,  3.0, 17.00,  3.5,  1.7,  8],
    [ 0.05, 10.0, 17.00,  0.1,  8.0, 14],
    [ 3.00,  3.5,  1.70, 10.0, 17.0,  8],
    [17.00,  8.0,  0.05, 10.0,  0.1, 14],
]).T[np.newaxis,:,:]
_P = np.array([
    [.1312, .1696, .5569, .0124, .8283, .5886],
    [.2329, .4135, .8307, .3736, .1004, .9991],
    [.2348, .1451, .3522, .2883, .3047, .6650],
    [.4047, .8828, .8732, .5743, .1091, .0381],
]).T[np.newaxis,:,:]
_four_nine_exp = np.exp(-4 / 9)


@row_vectorize
def hartmann6_hf(xx):
    # if xx.ndim == 2:
    #     return np.array([hartmann6_hf(x) for x in xx])

    xx = xx[:,:,np.newaxis]

    alpha = np.array([1, 1.2, 3, 3.2])[:,np.newaxis]

    tmp1 = (xx - _P)**2 * _A
    tmp2 = np.exp(-np.sum(tmp1, axis=1))
    # tmp3 = alpha.dot(tmp2) + 2.58
    tmp3 = tmp2.dot(alpha) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


@row_vectorize
def hartmann6_lf(xx):
    # if xx.ndim == 2:
    #     return np.array([hartmann6_lf(x) for x in xx])

    xx = xx[:,:,np.newaxis]

    alpha = np.array([0.5, 0.5, 2, 4])[:,np.newaxis]

    tmp1 = (xx - _P)**2 * _A
    tmp2 = f_exp(-np.sum(tmp1, axis=1))
    # tmp3 = alpha.dot(tmp2) + 2.58
    tmp3 = tmp2.dot(alpha) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


def f_exp(xx):

    return (_four_nine_exp + _four_nine_exp * (np.exp((xx + 4) / 9))) ** 9


l_bound = [0.1] * 6
u_bound = [1] * 6

hartmann6 = MultiFidelityFunction(
    u_bound, l_bound,
    [hartmann6_hf, hartmann6_lf],
    fidelity_names=['high', 'low']
)

