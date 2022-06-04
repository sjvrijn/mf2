# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Park ('91) B function as defined in:

    Shifeng Xiong, Peter Z. G. Qian & C. F. Jeff Wu (2013) Sequential
    Design and Analysis of High-Accuracy and Low-Accuracy Computer
    Codes, Technometrics, 55:1, 37-46, DOI: 10.1080/00401706.2012.723572

Function definitions:

.. math::

    f_h(x_1, x_2, x_3, x_4) = \dfrac{2}{3}\exp(x_1 + x_2) - x_4\sin(x_3) + x_3

.. math::

    f_l(x_1, x_2, x_3, x_4) = 1.2f_h(x_1, x_2, x_3, x_4) - 1


Adapted from matlab implementation at

    https://www.sfu.ca/~ssurjano/park91b.html, retrieved 2017-10-02

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


def park91b_hf(xx):
    """
    PARK (1991) FUNCTION 2

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    xx = np.atleast_2d(xx)

    x1, x2, x3, x4 = xx.T

    term1 = (2 / 3) * np.exp(x1 + x2)
    term2 = -x4 * np.sin(x3)
    term3 = x3

    return term1 + term2 + term3


def park91b_lf(xx):
    """
    PARK (1991) FUNCTION 2, LOWER FIDELITY CODE
    Calls: park91b_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function park91b_hf.

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    xx = np.atleast_2d(xx)

    yh = park91b_hf(xx)
    return 1.2 * yh - 1


#: Lower bound for Park91B function
l_bound = [0, 0, 0, 0]
#: Upper bound for Park91B function
u_bound = [1, 1, 1, 1]

x_opt = [0, 0, 0, 0]

#: 4D Park91B function with fidelities 'high' and 'low'
park91b = MultiFidelityFunction(
    "park91b",
    u_bound, l_bound,
    [park91b_hf, park91b_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
