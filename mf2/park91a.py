# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Park ('91) A function as defined in:

    Shifeng Xiong, Peter Z. G. Qian & C. F. Jeff Wu (2013) Sequential
    Design and Analysis of High-Accuracy and Low-Accuracy Computer
    Codes, Technometrics, 55:1, 37-46, DOI: 10.1080/00401706.2012.723572

Function definitions:

.. math::

    f_h(x_1, x_2, x_3, x_4) = \dfrac{x_1}{2} \Bigg(\sqrt{1 + (x_2 + x_3^2) *
                              \dfrac{x_4}{x_1^2}} - 1\Bigg) +
                              (x_1 + 3x_4)\exp(1 + \sin(x_3))

.. math::

    f_l(x_1, x_2, x_3, x_4) = (1+\sin(x_1) / 10)f_h(x_1, x_2, x_3, x_4) +
                              -2x_1 + x_2^2 + x_3^2 + 0.5


Adapted from matlab implementation at

    https://www.sfu.ca/~ssurjano/park91a.html, retrieved 2017-10-02

by: Sonja Surjanovic and Derek Bingham, Simon Fraser University

Copyright 2013. Derek Bingham, Simon Fraser University.

THERE IS NO WARRANTY, EXPRESS OR IMPLIED. WE DO NOT ASSUME ANY LIABILITY
FOR THE USE OF THIS SOFTWARE.  If software is modified to produce
derivative works, such modified software should be clearly marked.
Additionally, this program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; version 2.0 of the License.
Accordingly, this program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


def park91a_hf(xx):
    """
    PARK (1991) FUNCTION 1

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    xx = np.atleast_2d(xx)

    x1, x2, x3, x4 = xx.T

    term1a = x1 / 2
    term1b = np.sqrt(1 + (x2 + x3 ** 2) * x4 / (x1 ** 2)) - 1
    term1 = term1a * term1b

    term2a = x1 + 3 * x4
    term2b = np.exp(1 + np.sin(x3))
    term2 = term2a * term2b

    return term1 + term2


def park91a_lf(xx):
    """
    PARK (1991) FUNCTION 1, LOWER FIDELITY CODE
    Calls: park91a_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function park91a_hf.

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    xx = np.atleast_2d(xx)

    x1, x2, x3, _ = xx.T
    yh = park91a_hf(xx)

    term1 = (1 + np.sin(x1) / 10) * yh
    term2 = -2 * x1 + x2 ** 2 + x3 ** 2

    return term1 + term2 + 0.5


#: Lower bound for Park91A function
l_bound = [1e-8, 0, 0, 0]
#: Upper bound for Park91A function
u_bound = [1, 1, 1, 1]

x_opt = [1e-8, 0, 0, 0]

#: 4D Park91A function with fidelities 'high' and 'low'
park91a = MultiFidelityFunction(
    "park91a",
    u_bound, l_bound,
    [park91a_hf, park91a_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
