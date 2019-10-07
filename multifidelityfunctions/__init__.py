#!/usr/bin/python3
# -*- coding: utf-8 -*-
from .multiFidelityFunction import MultiFidelityFunction, row_vectorize
from .artificialMultifidelity import artificial_multifidelity
from .borehole import borehole
from .curretal88exp import currin
from .park91a import park91a
from .park91b import park91b
from .paciorek import adjustable_paciorek
from .BC import bohachevsky
from .BR import adjustable_branin, branin
from .BT import booth
from .FR import forrester
from .HM import himmelblau, himmelblau_3f
from .HMseb import himmelblau_seb
from .SC import sixHumpCamelBack
from .Hartmann import adjustable_hartmann3, hartmann6

"""
multifidelityfunctions

A collection of analytical functions with 2 or more available fidelities.
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'

bi_fidelity = [
    'borehole',
    'curretal88exp',
    'park91a',
    'park91b',
    'forrester',
    'hartmann3',
    'hartmann6',
    'bohachevsky',
    'branin',
    'booth',
    'sixHumpCamelBack',
]

tri_fidelity = [
    'himmelblau',
    'himmelblau_seb',
]

six_fidelity = [
    'artificial_multifidelity',
]

arbitrary_fidelity = [
]


__all__ = bi_fidelity + tri_fidelity + six_fidelity + arbitrary_fidelity
