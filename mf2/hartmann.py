# -*- coding: utf-8 -*-

r"""
hartmann.py: contains the Hartmann6 function

As defined in

    "Remarks on multi-fidelity surrogates" by Chanyoung Park, Raphael T. Haftka
    and Nam H. Kim (2016)

Function definitions:

.. math::

    f_h(x_1, ..., x_6) = -\dfrac{1}{1.94}\Bigg( 2.58 + \sum^4_{i=1}\alpha_i
    \exp\Big( -\sum^6_{j=1} A_{ij}(x_j - P_{ij})^2 \Big) \Bigg)

.. math::

    f_l(x_1, ..., x_6) = -\dfrac{1}{1.94}\Bigg( 2.58 + \sum^4_{i=1}\alpha^{\prime}_i
    f_{exp}\Big( -\sum^6_{j=1} A_{ij}(x_j - P_{ij})^2 \Big) \Bigg)

.. math::

    f_{exp}(x) = (\exp(-4/9) + (\exp(-4/9) * (x + 4)/9)) ^ 9

with the following matrices and vectors:

.. math::

    A = \left( \begin{array}{cccccc}
        10    &  3   & 17    &  3.5 &  1.7 &  8 \\
         0.05 & 10   & 17    &  0.1 &  8   & 14 \\
         3    &  3.5 &  1.70 & 10   & 17   &  8 \\
        17    &  8   &  0.05 & 10   &  0.1 & 14
        \end{array} \right)

.. math::

    P = 10^{-4}\left( \begin{array}{cccccc}
        1312 & 1696 & 5569 &  124 & 8283 & 5886 \\
        2329 & 4135 & 8307 & 3736 & 1004 & 9991 \\
        2348 & 1451 & 3522 & 2883 & 3047 & 6650 \\
        4047 & 8828 & 8732 & 5743 & 1091 &  381 \\
        \end{array} \right)

.. math::

    \alpha = \{0.5, 0.5, 2.0, 4.0\}

    \alpha^{\prime} = \{1.0, 1.2, 3.0, 3.2\}
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction

# Some constant values for the Hartmann 6d calculations
_alpha6_low = np.array([0.5, 0.5, 2.0, 4.0])[:, np.newaxis]
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


def hartmann6_hf(xx):
    xx = np.atleast_2d(xx)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P6) ** 2 * _A6
    tmp2 = np.exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha6_high) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


def hartmann6_lf(xx):
    xx = np.atleast_2d(xx)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - _P6) ** 2 * _A6
    tmp2 = _f_exp(-np.sum(tmp1, axis=1))
    tmp3 = tmp2.dot(_alpha6_low) + 2.58

    return -(1/1.94) * tmp3.reshape((-1,))


def _f_exp(xx):
    return (_four_nine_exp + (_four_nine_exp * (xx + 4)/9)) ** 9


#: Lower bound for Hartmann6 function
l_bound = [0.1] * 6
#: Upper bound for Hartmann6 function
u_bound = [1] * 6

x_opt = [0.2017, 0.1500, 0.4769, 0.2753, 0.3117, 0.6573]

#: 6D Hartmann6 function with fidelities 'high' and 'low'
hartmann6 = MultiFidelityFunction(
    "Hartmann6",
    u_bound, l_bound,
    [hartmann6_hf, hartmann6_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
