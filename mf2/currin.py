# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Currin function as defined in:

    Shifeng Xiong, Peter Z. G. Qian & C. F. Jeff Wu (2013) Sequential
    Design and Analysis of High-Accuracy and Low-Accuracy Computer
    Codes, Technometrics, 55:1, 37-46, DOI: 10.1080/00401706.2012.723572

Function definitions:

.. math::

    f_h(x_1, x_2) = \Bigg( 1 - \exp(-\dfrac{1}{2x_2})\Bigg) \dfrac{2300x_1^3 +
                    1900x_1^2 + 2092x_1 + 60}{100x_1^3 + 500x_1^2 + 4x_1 + 20}

.. math::

    f_l(x_1, x_2) = (&f_h(x_1+0.05, x_2+0.05) + \\
                     &f_h(x_1+0.05, x_2-0.05) + \\
                     &f_h(x_1-0.05, x_2+0.05) + \\
                     &f_h(x_1-0.05, x_2-0.05)) / 4

Adapted from matlab implementation at

    https://www.sfu.ca/~ssurjano/curretal88exp.html, retrieved 2017-10-02

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


def currin_hf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    are_zero = x2 <= 1e-8  # Assumes x2 approaches 0 from positive
    fact1 = np.ones(x2.shape)

    fact1[~are_zero] -= np.exp(-1 / (2*x2[~are_zero]))

    # if abs(x2) <= 1e-8:
    #     fact1 = 1
    # else:        # Prevents division by 0 error/warning
    #     fact1 = 1 - np.exp(-1 / (2*x2))

    fact2 = 2300*(x1 ** 3) + 1900*(x1 ** 2) + 2092*x1 + 60
    fact3 = 100*(x1 ** 3) + 500*(x1 ** 2) + 4*x1 + 20

    return fact1 * fact2 / fact3


def currin_lf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION, LOWER FIDELITY CODE
    Calls: currin_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function currin_hf.

    INPUT:
    xx = [x1, x2]
    """
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T

    x1_plus = (x1 + .05).reshape(-1,1)
    x1_minus = (x1 - .05).reshape(-1,1)
    x2_plus = (x2 + .05).reshape(-1,1)
    x2_minus = (x2 - .05).reshape(-1,1)
    x2_minus[x2_minus < 0] = 0

    yh1 = currin_hf(np.hstack([x1_plus, x2_plus]))
    yh2 = currin_hf(np.hstack([x1_plus, x2_minus]))
    yh3 = currin_hf(np.hstack([x1_minus, x2_plus]))
    yh4 = currin_hf(np.hstack([x1_minus, x2_minus]))

    return (yh1 + yh2 + yh3 + yh4) / 4


#: Lower bound for Currin function
l_bound = [0, 0]
#: Upper bound for Currin function
u_bound = [1, 1]

x_opt = [0.21666666666666, 0]

#: 2D Currin function with fidelities 'high' and 'low'
currin = MultiFidelityFunction(
    "currin",
    u_bound, l_bound,
    [currin_hf, currin_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
