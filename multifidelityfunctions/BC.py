#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from .multiFidelityFunction import BiFidelityFunction, row_vectorize

"""
BC.py:
Bohachevsky function

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


def bohachevsky_hf(xx):
    """
    BOHACHEVSKY FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1 = x1**2 + 2*x2**2
    term2 = 0.3*math.cos(3*math.pi*x1)
    term3 = 0.4*math.cos(4*math.pi*x2)

    return term1 - term2 - term3 + 0.7


def bohachevsky_lf(xx):
    """
    BOHACHEVSKY FUNCTION, LOWER FIDELITY CODE
    Calls: bohachevsky_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function bohachevsky_hf.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1 = bohachevsky_hf([0.7*x1, x2])
    term2 = x1*x2 - 12

    return term1 + term2


l_bound = [-5, -5]
u_bound = [ 5,  5]

bohachevsky = BiFidelityFunction(
    u_bound, l_bound,
    row_vectorize(bohachevsky_hf),
    row_vectorize(bohachevsky_lf),
)
