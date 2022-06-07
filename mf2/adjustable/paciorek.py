# -*- coding: utf-8 -*-

r"""Implementation of the adjustable bi-fidelity Paciorek function
as defined in:

    Toal, D.J.J. Some considerations regarding the use of multi-
    fidelity Kriging in the construction of surrogate models.
    Struct Multidisc Optim 51, 1223–1245 (2015)
    doi:10.1007/s00158-014-1209-5

Function definitions:

.. math::

    f_h(x_1, x_2) = \sin \Big( \dfrac{1}{x_1x_2} \Big)

.. math::

    f_l(x_1, x_2) = f_h(x_1, x_2) - 9a^2\cos \Big( \dfrac{1}{x_1x_2} \Big)

where :math:`a \in (0, 1]` is the adjustable parameter
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

x_opt = [0.460658865961780639020326, 0.460658865961780639020326]  # sqrt(3pi/2)

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
    x_opt=x_opt,
)
