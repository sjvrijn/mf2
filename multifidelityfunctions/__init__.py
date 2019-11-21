# -*- coding: utf-8 -*-

"""
multifidelityfunctions

A collection of analytical functions with 2 or more available fidelities.
"""

from .multiFidelityFunction import MultiFidelityFunction, row_vectorize
from .artificialMultifidelity import artificial_multifidelity
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

import multifidelityfunctions.adjustable

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'
__version__ = '2019.11.1'


bi_fidelity_functions = (
    borehole,
    currin,
    park91a,
    park91b,
    forrester,
    Forrester,
    hartmann6,
    himmelblau,
    bohachevsky,
    branin,
    booth,
    six_hump_camelback,
)

tri_fidelity_functions = (
    himmelblau_3f,
    himmelblau_seb,
)

six_fidelity_functions = (
    artificial_multifidelity,
)
