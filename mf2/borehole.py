# -*- coding: utf-8 -*-

r"""Implementation of the bi-fidelity Borehole function as defined in:

    Shifeng Xiong, Peter Z. G. Qian & C. F. Jeff Wu (2013) Sequential
    Design and Analysis of High-Accuracy and Low-Accuracy Computer
    Codes, Technometrics, 55:1, 37-46, DOI: 10.1080/00401706.2012.723572

Function definitions:

.. math::

    f_b(x, A, B) =
    \dfrac{A*T_u*(H_u - H_l)}{\Bigg(\log(\frac{r}{r_w}) *
    (B + \dfrac{2L*T_u}{\log(\frac{r}{r_w}) * r_w^2 * K_w} +
    \dfrac{T_u}{T_l}\Bigg)}

.. math::

    f_h(x) = f_b(x, 2\pi, 1)

.. math::

    f_l(x) = f_b(x, 5, 1.5)


Adapted from matlab implementation at

    https://www.sfu.ca/~ssurjano/borehole.html, retrieved 2017-10-02

by: Sonja Surjanovic and Derek Bingham, Simon Fraser University

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
"""

import numpy as np

from .multi_fidelity_function import MultiFidelityFunction


_tau = 2*np.pi


def _borehole_base(xx, a, b):
    xx = np.atleast_2d(xx)

    rw, r, Tu, Hu, Tl, Hl, L, Kw = xx.T

    frac1 = a * Tu * (Hu - Hl)

    frac2a = 2*L*Tu / (np.log(r/rw) * (rw**2) * Kw)
    frac2b = Tu / Tl
    frac2 = np.log(r/rw) * (b + frac2a + frac2b)

    return frac1 / frac2


def borehole_hf(xx):
    """
        BOREHOLE FUNCTION

        INPUT AND OUTPUT:
        inputs = [rw, r, Tu, Hu, Tl, Hl, L, Kw]
        output = water flow rate
    """
    return _borehole_base(xx, a=_tau, b=1)


def borehole_lf(xx):
    """
        BOREHOLE FUNCTION, LOWER FIDELITY CODE
        This function is used as the "low-accuracy code" version of the function
        borehole_hf.

        INPUT AND OUTPUT:
        inputs = [rw, r, Tu, Hu, Tl, Hl, L, Kw]
        output = water flow rate
    """
    return _borehole_base(xx, a=5, b=1.5)


#: Lower bound for Borehole function
l_bound = [0.05,    100,  63_070,   990, 63.1, 700, 1_120,  9_855]
#: Upper bound for Borehole function
u_bound = [0.15, 50_000, 115_600, 1_110,  116, 820, 1_680, 12_045]

x_opt = [5e-2, 5e4, 6.307e4, 9.9e2, 6.31e1, 8.2e2, 1.68e3, 9.855e3]

#: 8D Borehole function with fidelities 'high' and 'low'
borehole = MultiFidelityFunction(
    "borehole",
    u_bound, l_bound,
    [borehole_hf, borehole_lf],
    fidelity_names=['high', 'low'],
    x_opt=x_opt,
)
