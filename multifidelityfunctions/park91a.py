#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize

"""
park91a.py:
PARK (1991) FUNCTION 1

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
def park91a_hf(xx):
    """
    PARK (1991) FUNCTION 1

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    x1, x2, x3, x4 = xx.T

    term1a = x1 / 2
    term1b = np.sqrt(1 + (x2 + x3 ** 2) * x4 / (x1 ** 2)) - 1
    term1 = term1a * term1b

    term2a = x1 + 3 * x4
    term2b = np.exp(1 + np.sin(x3))
    term2 = term2a * term2b

    return term1 + term2


@row_vectorize
def park91a_lf(xx):
    """
    PARK (1991) FUNCTION 1, LOWER FIDELITY CODE
    Calls: park91a_hf
    This function, from Xiong et al. (2013), is used as the "low-accuracy
    code" version of the function park91a_hf.

    INPUT:
    xx = [x1, x2, x3, x4]
    """
    x1, x2, x3, x4 = xx.T
    yh = park91a_hf(xx)

    term1 = (1 + np.sin(x1) / 10) * yh
    term2 = -2 * x1 + x2 ** 2 + x3 ** 2

    return term1 + term2 + 0.5


l_bound = [1e-8, 0, 0, 0]
u_bound = [1, 1, 1, 1]

park91a = MultiFidelityFunction(
    u_bound, l_bound,
    [park91a_hf, park91a_lf],
    fidelity_names=['high', 'low']
)
