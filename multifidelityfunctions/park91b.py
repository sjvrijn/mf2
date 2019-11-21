# -*- coding: utf-8 -*-

"""
park91b.py:
PARK (1991) FUNCTION 2

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

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize


@row_vectorize
def park91b_hf(xx):
    """
    PARK (1991) FUNCTION 2

    INPUT:
    xx = [x1, x2, x3, x4]
    """

    x1, x2, x3, x4 = xx.T

    term1 = (2 / 3) * np.exp(x1 + x2)
    term2 = -x4 * np.sin(x3)
    term3 = x3

    return term1 + term2 + term3


@row_vectorize
def park91b_lf(xx):
    """
    PARK (1991) FUNCTION 2, LOWER FIDELITY CODE
    Calls: park91b_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function park91b_hf.

    INPUT:
    xx = [x1, x2, x3, x4]
    """

    yh = park91b_hf(xx)
    return 1.2 * yh - 1


l_bound = [0, 0, 0, 0]
u_bound = [1, 1, 1, 1]

park91b = MultiFidelityFunction(
    "park 91b",
    u_bound, l_bound,
    [park91b_hf, park91b_lf],
    fidelity_names=['high', 'low']
)
