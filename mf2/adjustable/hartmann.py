# -*- coding: utf-8 -*-

r"""Implementation of the adjustable bi-fidelity Hartmann3 function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5

Function definitions:

.. math::

    f_h(x_1, x_2, x_3) = -\sum^4_{i=1} \alpha_i \exp \Bigg(-\sum^3_{j=1} \beta_{ij}
                         (x_j - P_{ij})^2 \Bigg)

.. math::

    f_l(x_1, x_2, x_3) = -\sum^4_{i=1} \alpha_i \exp \Bigg(-\sum^3_{j=1} \beta_{ij}
                         \Big(x_j - \dfrac{3}{4}P_{ij}(a + 1)\Big)^2 \Bigg)

with the following matrices and vectors:

.. math::

    \beta = \left( \begin{array}{cccccc}
        3   & 10 & 30 \\
        0.1 & 10 & 35 \\
        3   & 10 & 30 \\
        0.1 & 10 & 35
        \end{array} \right)

.. math::

    P = 10^{-4} \left( \begin{array}{cccccc}
        3689 & 1170 & 2673 \\
        4699 & 4387 & 7470 \\
        1091 & 8732 & 5547 \\
         381 & 5743 & 8828
        \end{array} \right)

.. math::

    \alpha = \{1.0, 1.2, 3.0, 3.2\}

and where :math:`a \in [0, 1]` is the adjustable parameter.
"""


import numpy as np

from mf2.multi_fidelity_function import AdjustableMultiFidelityFunction


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


def adjustable_hartmann3_lf(xx, a):
    xx = np.atleast_2d(xx)

    factor = 3/4 * (a + 1)

    xx = xx[:,:,np.newaxis]

    tmp1 = (xx - (_P3 * factor))
    tmp2 = tmp1 ** 2 * _beta3
    tmp3 = np.exp(-np.sum(tmp2, axis=1))
    tmp4 = tmp3.dot(_alpha3)

    return -tmp4.reshape((-1,))


u_bound = [1]*3
l_bound = [0]*3

x_opt = [0.11458889011259411, 0.5556488928818787, 0.852546981666729]

docstring = """Factory method for adjustable Hartmann3 function using parameter value `a3`

    :param a3:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1]. High- and low-
                fidelity are identical for `a3=1/3`.
    :return:    A MultiFidelityFunction instance
    """

hartmann3 = AdjustableMultiFidelityFunction(
    "Hartmann3",
    u_bound, l_bound,
    [hartmann3_hf],
    [adjustable_hartmann3_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
