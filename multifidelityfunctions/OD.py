#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from .multiFidelityFunction import row_vectorize, MultiFidelityFunction

"""
OD.py:
Forrester et al. (2007) One-dimensional mulfi-fidelity function

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


@row_vectorize
def oneDimensional_hf(xx):
    """
    ONE DIMENSIONAL FUNCTION

    INPUT:
    xx = [x1]
    """

    term1 = (6*xx - 2)**2
    term2 = math.sin(12*xx - 4)

    return term1 * term2


@row_vectorize
def oneDimensional_lf(xx):
    """
    ONE DIMENSIONAL FUNCTION, LOWER FIDELITY CODE
    Calls: oneDimensional_hf
    This function is used as the "low-accuracy code" version of the function oneDimensional_hf.

    INPUT:
    xx = [x1]
    """

    term1 = 0.5*oneDimensional_hf(xx)
    term2 = 10*(xx - 0.5) - 5

    return term1 + term2


l_bound = [0]
u_bound = [1]

oneDimensional = MultiFidelityFunction(
    u_bound, l_bound,
    [oneDimensional_hf, oneDimensional_lf],
    fidelity_names=['high', 'low']
)
