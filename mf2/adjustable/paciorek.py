# -*- coding: utf-8 -*-

"""
paciorek.py: contains the Paciorek 2d function

As defined in "Some Considerations Regarding the Use of Multi-fidelity Kriging
in the Construction of Surrogate Models" by David J.J. Toal (2015)
"""

from functools import partial

import numpy as np

from mf2.multiFidelityFunction import MultiFidelityFunction


def paciorek_hf(xx):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    return np.sin(1/(x1*x2))


def adjustable_paciorek_lf(xx, a2):
    xx = np.atleast_2d(xx)

    x1, x2 = xx.T
    temp1 = paciorek_hf(xx)
    temp2 = 9 * a2**2
    temp3 = np.cos(1/(x1*x2))
    return temp1 - (temp2*temp3)


def paciorek(a2):
    return MultiFidelityFunction(
        f"adjustable Paciorek {a2}",
        [1]*2, [0.3]*2,
        [paciorek_hf, partial(adjustable_paciorek_lf, a2=a2)],
        fidelity_names=['high', 'low'],
    )
