#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize

"""
BR.py:
Branin function

Authors: Sander van Rijn, Leiden University


THERE IS NO WARRANTY, EXPRESS OR IMPLIED. WE DO NOT ASSUME ANY LIABILITY
FOR THE USE OF THIS SOFTWARE.  If software is modified to produce
derivative works, such modified software should be clearly marked.
Additionally, this program is free software you can redistribute it
and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation version 2.0 of the License.
Accordingly, this program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
"""


_four_pi_square = 4*np.pi**2
_eight_pi = 8*np.pi


@row_vectorize
def branin_base(xx):
    """
    BRANIN FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx.T

    # t = 1 / (8 * math.pi**2)
    # s = 10
    # r = 6
    # c = 5 / math.pi
    # b = 5.1 / (4 * math.pi**2)
    # a = 1
    #
    # term1 = a * (x2 - b * x1**2 + c * x1 - r)**2
    # term2 = s * (1 - t) * math.cos(x1)
    #
    # return term1 + term2 + s

    term1 = x2 - (5.1 * (x1**2 / _four_pi_square)) + ((5*x1) / np.pi) - 6
    term2 = (10 * np.cos(x1)) * (1 - (1/_eight_pi))

    return term1**2 + term2 + 10


@row_vectorize
def branin_hf(xx):
    """
    BRANIN FUNCTION, HIGH FIDELITY CODE
    Calls: branin_base
    This function, from Dong et al. (2015), is used as the "high-accuracy code"
    version of the function based on the 'traditional' branin function.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx.T
    return branin_base(xx) - 2.25*x2  # 22.5


@row_vectorize
def branin_lf(xx):
    """
    BRANIN FUNCTION, LOWER FIDELITY CODE
    Calls: branin_base
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function branin_hf.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx.T

    term1 = branin_base(np.hstack([0.7*x1.reshape(-1,1), 0.7*x2.reshape(-1,1)]))
    term2 = 1.575*x2  # 15.75
    term3 = 2*(.9+x1**2)
    term4 = 50

    return term1 - term2 + term3 - term4


l_bound = [-5,  0]
u_bound = [10, 15]

branin = MultiFidelityFunction(
    "branin",
    u_bound, l_bound,
    [branin_hf, branin_lf],
    fidelity_names=['high', 'low']
)
