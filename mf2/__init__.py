# -*- coding: utf-8 -*-

"""
mf2

A collection of analytical functions with 2 or more available fidelities.
"""

from .multiFidelityFunction import MultiFidelityFunction
from .borehole import borehole
from .currin import currin
from .park91a import park91a
from .park91b import park91b
from .bohachevsky import bohachevsky
from .branin import branin
from .booth import booth
from .forrester import forrester, Forrester
from .himmelblau import himmelblau, himmelblau_3f
from .himmelblau_seb import himmelblau_seb
from .six_hump_camelback import six_hump_camelback
from .hartmann import hartmann6

import mf2.adjustable

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'
with open('VERSION') as f:
    __version__ = f.readline()


bi_fidelity_functions = (
    # 1D
    forrester,
    # 2D
    bohachevsky,
    booth,
    branin,
    currin,
    himmelblau,
    six_hump_camelback,
    # 4D
    park91a,
    park91b,
    # 6D
    hartmann6,
    # 8D
    borehole,
)

tri_fidelity_functions = (
    himmelblau_3f,
    himmelblau_seb,
)
