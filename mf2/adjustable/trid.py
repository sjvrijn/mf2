# -*- coding: utf-8 -*-

"""
trid.py: contains the Trid 10d function

As defined in "Some Considerations Regarding the Use of Multi-fidelity Kriging
in the Construction of Surrogate Models" by David J.J. Toal (2015)
"""

from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction, row_vectorize


@row_vectorize
def trid_hf(xx):
    temp1 = np.sum((xx - 1) ** 2, axis=1)
    temp2 = np.sum(xx[:,:-1] * xx[:,1:], axis=1)
    return temp1 - temp2

@row_vectorize
def adjustable_trid_lf(xx, a4):
    temp1 = np.sum((xx - a4) ** 2, axis=1)
    temp2 = np.sum((a4-0.65) * xx[:,:-1] * xx[:,1:] * np.arange(2, 11), axis=1)
    return temp1 - temp2


def trid(a4):
    return MultiFidelityFunction(
        f"adjustable Trid {a4}",
        [1]*10, [0]*10,
        [trid_hf, partial(adjustable_trid_lf, a4=a4)],
        fidelity_names=['high', 'low'],
    )
