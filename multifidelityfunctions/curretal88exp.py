#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize

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


@row_vectorize
def currin_hf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION

    INPUT:
    xx = [x1, x2]
    """
    x1, x2 = xx.T

    are_zero = x2 <= 1e-8
    fact1 = np.ones(x2.shape)

    fact1[~are_zero] -= np.exp(-1 / (2*x2[~are_zero]))

    # if abs(x2) <= 1e-8:  # Assumes x2 approaches 0 from positive
    #     fact1 = 1
    # else:        # Prevents division by 0 error/warning
    #     fact1 = 1 - np.exp(-1 / (2*x2))

    fact2 = 2300*(x1 ** 3) + 1900*(x1 ** 2) + 2092*x1 + 60
    fact3 = 100*(x1 ** 3) + 500*(x1 ** 2) + 4*x1 + 20

    return fact1 * fact2 / fact3


@row_vectorize
def currin_lf(xx):
    """
    CURRIN ET AL. (1988) EXPONENTIAL FUNCTION, LOWER FIDELITY CODE
    Calls: currin_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function currin_hf.

    INPUT:
    xx = [x1, x2]
    """
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


l_bound = [0, 0]
u_bound = [1, 1]

currin = MultiFidelityFunction(
    u_bound, l_bound,
    [currin_hf, currin_lf],
    fidelity_names=['high', 'low']
)
