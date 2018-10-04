#!/usr/bin/python
# -*- coding: utf-8 -*-

from MultiFidelityFunctions import BiFidelityFunction

"""
BT.py:
Booth function

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


def booth_hf(xx):
    """
    BOOTH FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1 = (x1 + 2*x2 - 7)**2
    term2 = (2*x1 + x2 - 5)**2

    return term1 + term2


def booth_lf(xx):
    """
    BOOTH FUNCTION, LOWER FIDELITY CODE
    Calls: booth_hf
    This function, from Dong et al. (2015), is used as the "low-accuracy code"
    version of the function booth_hf.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    term1 = booth_hf([0.4*x1, x2])
    term2 = 1.7*x1*x2 - x1 + 2*x2

    return term1 + term2


l_bound = [-10, -10]
u_bound = [ 10,  10]

booth = BiFidelityFunction(u_bound, l_bound, booth_hf, booth_lf)
