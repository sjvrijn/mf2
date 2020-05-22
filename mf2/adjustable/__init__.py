# -*- coding: utf-8 -*-

"""
adjustable/: correlation-adjustable multi-fidelity functions.
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


from .branin import branin
from .hartmann import hartmann3
from .paciorek import paciorek
from .trid import trid


bi_fidelity_functions = (
    branin,
    paciorek,
    hartmann3,
    trid,
)
