#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

from multifidelityfunctions import BiFidelityFunction

"""
curretal88exp.py:
CURRIN ET AL. (1988) EXPONENTIAL FUNCTION

Authors: Sonja Surjanovic, Simon Fraser University
         Derek Bingham, Simon Fraser University
         Sander van Rijn, Leiden University (Python port)
Questions/Comments: Please email Derek Bingham at dbingham@stat.sfu.ca.

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

For function details and reference information, see:
http://www.sfu.ca/~ssurjano/
"""


def curretal88exp_hf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx

    fact1 = 1 - math.exp(-1 / (2 * x2))
    fact2 = 2300 * (x1 ** 3) + 1900 * (x1 ** 2) + 2092 * x1 + 60
    fact3 = 100 * (x1 ** 3) + 500 * (x1 ** 2) + 4 * x1 + 20

    return fact1 * fact2 / fact3


def curretal88exp_lf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION, LOWER FIDELITY CODE
    Calls: curretal88exp_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function curretal88exp_hf.

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx
    maxarg = max(0.001, x2 - 1 / 20)  # TODO: '0.001' was originally '0', but caused divide by zero errors

    yh1 = curretal88exp_hf( [x1+1 / 20, x2+1 / 20] )
    yh2 = curretal88exp_hf( [x1+1 / 20, maxarg] )
    yh3 = curretal88exp_hf( [x1-1 / 20, x2+1 / 20] )
    yh4 = curretal88exp_hf( [x1-1 / 20, maxarg] )

    return (yh1 + yh2 + yh3 + yh4) / 4


l_bound = [0, 0]
u_bound = [1, 1]

curretal88exp = BiFidelityFunction(u_bound, l_bound, curretal88exp_hf, curretal88exp_lf)
