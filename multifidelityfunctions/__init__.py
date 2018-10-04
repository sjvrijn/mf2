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
from .SC import *

u"""
MultiFidelityFunctions

A collection of analytical functions with 2 or more available fidelities.
"""

__author__ = u'Sander van Rijn'
__email__ = u's.j.van.rijn@liacs.leidenuniv.nl'

bi_fidelity = [
    'borehole',
    'curretal88exp',
    'park91a',
    'park91b',
    'oneDimensional',
    'bohachevsky',
    'branin',
    'booth',
    'himmelblau',
    'sixHumpCamelBack',
]

six_fidelity = [
    'artificial_multifidelity',
]


__all__ = bi_fidelity + six_fidelity
