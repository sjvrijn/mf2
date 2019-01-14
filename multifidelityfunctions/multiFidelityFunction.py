#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
from numbers import Integral
import numpy as np

BiFidelityFunction = namedtuple('BiFidelityFunction', ['u_bound', 'l_bound', 'high', 'low'])
TriFidelityFunction = namedtuple('TriFidelityFunction', ['u_bound', 'l_bound', 'high', 'medium', 'low'])


@property
def _ndim(self):
    return len(self.u_bound)


@property
def _fidelity_names(self):
    for field in self._fields:
        if 'bound' not in field:
            yield field


BiFidelityFunction.ndim = _ndim
TriFidelityFunction.ndim = _ndim

BiFidelityFunction.fidelity_names = _fidelity_names
TriFidelityFunction.fidelity_names = _fidelity_names


def row_vectorize(func):
    def new_func(X):
        try:
            return np.array([func(row) for row in X])
        except TypeError:
            return func(X)
    return new_func


class MultiFidelityFunction:


    def __init(self, u_bound, l_bound, functions, fidelity_names=None):
        self.u_bound = u_bound
        self.l_bound = l_bound

        self.functions = functions
        if fidelity_names:
            # dict-style name-indexing
            self.fidelity_names = fidelity_names
            self.fidelity_dict = dict(zip(fidelity_names, functions))
            # class-style indexing
            for name, func in zip(fidelity_names, functions):
                setattr(self, name, func)
        else:
            self.fidelity_dict = None
            self.fidelity_names = None




    @property
    def ndim(self):
        return len(self.u_bound)


    def __getitem__(self, item):
        if isinstance(item, Integral):
            return self.functions[item]
        elif isinstance(item, str) and self.fidelity_dict:
            return self.fidelity_dict[item]
        else:
            raise ValueError(f'Invalid index')
