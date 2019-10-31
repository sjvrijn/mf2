#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .multiFidelityFunction import MultiFidelityFunction, row_vectorize
from .artificialMultifidelity import artificial_multifidelity
from .borehole import borehole
from .currin import currin
from .park91a import park91a
from .park91b import park91b
from .paciorek import adjustable_paciorek
from .trid import adjustable_trid
from .bohachevsky import bohachevsky
from .branin import adjustable_branin, branin
from .booth import booth
from .forrester import forrester
from .himmelblau import himmelblau, himmelblau_3f
from .himmelblau_seb import himmelblau_seb
from .six_hump_camelback import six_hump_camelback
from .hartmann import adjustable_hartmann3, hartmann6

"""
multifidelityfunctions

A collection of analytical functions with 2 or more available fidelities.
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'

bi_fidelity_functions = [
    borehole,
    currin,
    park91a,
    park91b,
    forrester,
    hartmann6,
    himmelblau,
    bohachevsky,
    branin,
    booth,
    six_hump_camelback,
]

adjustable_bifidelity_functions = [
    adjustable_branin,
    adjustable_paciorek,
    adjustable_hartmann3,
    adjustable_trid,
]

tri_fidelity_functions = [
    himmelblau_3f,
    himmelblau_seb,
]

six_fidelity_functions = [
    artificial_multifidelity,
]
