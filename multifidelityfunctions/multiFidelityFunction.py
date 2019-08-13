#!/usr/bin/python
# -*- coding: utf-8 -*-
from numbers import Integral
import numpy as np


# def new_vectorize(func):
def row_vectorize(func):
    def new_func(X):
        X = np.array(X)
        try:
            # print("try:", X)
            res = func(X)
            # print("tried:", res)
            return res
        except (np.AxisError, AttributeError, IndexError):
            # print("except:", X, X.reshape((1, -1)))
            res = func(X.reshape((1, -1)))
            # print("excepted", res)
            return res

    return new_func


# def row_vectorize(func):
#     def new_func(X):
#         try:
#             return np.array([func(row) for row in X])
#         except TypeError:
#             return func(X)
#     return new_func


class MultiFidelityFunction:

    def __init__(self, u_bound, l_bound, functions, fidelity_names=None):
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
