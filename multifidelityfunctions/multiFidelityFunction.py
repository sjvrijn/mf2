#!/usr/bin/python
# -*- coding: utf-8 -*-
from numbers import Integral
import numpy as np


def row_vectorize(func):
    def new_func(X):
        X = np.array(X)
        try:
            res = func(X)
            return res
        except (np.AxisError, AttributeError, IndexError):
            res = func(X.reshape((1, -1)))
            return res

    return new_func


class MultiFidelityFunction:

    def __init__(self, name, u_bound, l_bound, functions, fidelity_names=None):
        self.name = name.title().replace(' ', '').replace('-', '')
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
            raise IndexError(f"Invalid index '{item}'")


    def __repr__(self):
        return f"MultiFidelityFunction({self.name}, {self.u_bound}, {self.l_bound}, {self.fidelity_names})"
