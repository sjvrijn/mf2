#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from multifidelityfunctions.multiFidelityFunction import BiFidelityFunction

"""
borehole.py:
BOREHOLE FUNCTION

Authors: Sonja Surjanovic, Simon Fraser University
         Derek Bingham, Simon Fraser University
         Sander van Rijn, Leiden University (Python port)
Questions/Comments: Please email Derek Bingham at dbingham@stat.sfu.ca.

Copyright 2013. Derek Bingham, Simon Fraser University.

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

For function details and reference information, see:
http://www.sfu.ca/~ssurjano/
"""


def borehole_hf(xx):
    """
        BOREHOLE FUNCTION

        INPUT AND OUTPUT:
        inputs = [rw, r, Tu, Hu, Tl, Hl, L, Kw]
        output = water flow rate
    """
    rw, r, Tu, Hu, Tl, Hl, L, Kw = xx

    frac1 = 2 * math.pi * Tu * (Hu-Hl)

    frac2a = 2*L*Tu / (math.log(r/rw)*(rw**2)*Kw)
    frac2b = Tu / Tl
    frac2 = math.log(r/rw) * (1+frac2a+frac2b)

    return -(frac1 / frac2)


def borehole_lf(xx):
    """
        BOREHOLE FUNCTION, LOWER FIDELITY CODE
        This function is used as the "low-accuracy code" version of the function
        borehole_hf.

        INPUT AND OUTPUT:
        inputs = [rw, r, Tu, Hu, Tl, Hl, L, Kw]
        output = water flow rate
    """
    rw, r, Tu, Hu, Tl, Hl, L, Kw = xx

    frac1 = 5 * Tu * (Hu-Hl)

    frac2a = 2*L*Tu / (math.log(r/rw) * (rw**2) * Kw)
    frac2b = Tu/Tl
    frac2 = math.log(r/rw) * (1.5+frac2a+frac2b)

    return -(frac1 / frac2)


l_bound = [0.05,   100,  63070,  990, 63.1, 700, 1120,  9855]
u_bound = [0.15, 50000, 115600, 1110,  116, 820, 1680, 12045]

borehole = BiFidelityFunction(u_bound, l_bound, borehole_hf, borehole_lf)
