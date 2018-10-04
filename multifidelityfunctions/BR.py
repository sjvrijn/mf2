#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from multifidelityfunctions import BiFidelityFunction

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


def branin_hf(xx):
    """
    BRANIN FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1a = x1**2 / 4*math.pi**2
    term1b = 5*x1 / math.pi
    term1 = x2 - 5.1*term1a + term1b - 6

    term2 = 10*math.cos(x1) * (1 - 1/(8*math.pi))

    return 10 + term1**2 + term2 - 22.5*x2


def branin_lf(xx):
    """
    BRANIN FUNCTION, LOWER FIDELITY CODE
    Calls: branin_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function branin_hf.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1 = branin_hf([0.7*x1, 0.7*x2]) - 15.75*x2
    term2 = 20*(0.9 + x1)**2 - 50

    return term1 + term2


l_bound = [-5, 10]
u_bound = [ 0, 15]

branin = BiFidelityFunction(u_bound, l_bound, branin_hf, branin_lf)
