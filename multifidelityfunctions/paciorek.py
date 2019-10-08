#!/usr/bin/python3
# -*- coding: utf-8 -*-
from functools import partial

import numpy as np

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize
"""
paciorek.py: contains the Paciorek 2d function

As defined in "Some Considerations Regarding the Use of Multi-fidelity Kriging
in the Construction of Surrogate Models" by David J.J. Toal (2015)
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'

@row_vectorize
def paciorek_hf(xx):
    x1, x2 = xx.T
    return np.sin(1/(x1*x2))


@row_vectorize
def adjustable_paciorek_lf(xx, a2):
    x1, x2 = xx.T
    temp1 = paciorek_hf(xx)
    temp2 = 9 * a2**2
    temp3 = np.cos(1/(x1*x2))
    return temp1 - (temp2*temp3)


def adjustable_paciorek(a2):
    return MultiFidelityFunction(
        f"adjustable Paciorek {a2}",
        [1]*2, [0.3]*2,
        [paciorek_hf, partial(adjustable_paciorek_lf, a2=a2)],
        fidelity_names=['high', 'low'],
    )
