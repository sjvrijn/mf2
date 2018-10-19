#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import numpy as np

BiFidelityFunction = namedtuple('BiFidelityFunction', ['u_bound', 'l_bound', 'high', 'low'])
TriFidelityFunction = namedtuple('TriFidelityFunction', ['u_bound', 'l_bound', 'high', 'medium', 'low'])


@property
def _ndim(self):
    return len(self.u_bound)


BiFidelityFunction.ndim = _ndim
TriFidelityFunction.ndim = _ndim


def row_vectorize(func):
    def new_func(X):
        try:
            return np.array([func(row) for row in X])
        except TypeError:
            return func(X)
    return new_func
