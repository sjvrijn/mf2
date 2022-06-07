# -*- coding: utf-8 -*-

r"""Implementation of the adjustable bi-fidelity Branin function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5

Function definitions:

.. math::

    f_h(x_1, x_2) = \Bigg(x_2 - (5.1\dfrac{x_1^2}{4\pi^2}) + \dfrac{5x_1}{\pi} -
                    6\Bigg)^2 + \Bigg(10\cos(x_1) (1 - \dfrac{1}{8\pi}\Bigg) + 10

.. math::

    f_l(x_1, x_2) = f_h(x_1, x_2) - (a+0.5)\Bigg( \Bigg(x_2 -
                    (5.1\dfrac{x_1^2}{4\pi^2}) + \dfrac{5x_1}{\pi} -
                    6\Bigg)^2 \Bigg)

where :math:`a \in [0, 1]` is the adjustable parameter.

Note that :math:`f_h` is equal to the non-adjustable :math:`f_b` defined in
:py:mod:`mf2.branin`.
"""


import numpy as np

from mf2.multi_fidelity_function import AdjustableMultiFidelityFunction
from mf2.branin import branin_base, l_bound, u_bound


_four_pi_square = 4*np.pi**2


def adjustable_branin_lf(xx, a):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    term1 = branin_base(xx)
    term2 = x2 - (5.1 * (x1**2 / _four_pi_square)) + ((5*x1) / np.pi) - 6

    return term1 - (a + 0.5) * term2 ** 2


x_opt = [np.pi, 2.275]  # one of three optima

docstring = """Factory method for adjustable Branin function using parameter value `a1`

    :param a1:  Parameter to tune the correlation between high- and low-fidelity
                functions. Expected values lie in range [0, 1]. High- and low-
                fidelity are identical for `a1=-0.5`.
    :return:    A MultiFidelityFunction instance
    """

branin = AdjustableMultiFidelityFunction(
    "Branin",
    u_bound, l_bound,
    static_functions=[branin_base],
    adjustable_functions=[adjustable_branin_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
