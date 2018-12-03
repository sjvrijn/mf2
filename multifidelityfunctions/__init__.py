#!/usr/bin/python
# -*- coding: utf-8 -*-
from .artificialMultifidelity import *
from .borehole import *
from .curretal88exp import *
from .park91a import *
from .park91b import *
from .OD import *
from .BC import *
from .BR import *
from .BT import *
from .HM import *
from .HMseb import *
from .SC import *

u"""
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
    'oneDimensional',
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


__all__ = bi_fidelity + tri_fidelity + six_fidelity
