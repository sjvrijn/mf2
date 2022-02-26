# -*- coding: utf-8 -*-

"""
multiFidelityFunction.py:

Defines the MultiFidelityFunction class for encapsuling all fidelities and
parameters of a multi-fidelity function. Also contains any other utility
functions that are commonly used by the various mf-functions in this package.
"""

from numbers import Integral
from typing import Callable
from warnings import warn

import numpy as np


class MultiFidelityFunction:

    def __init__(self, name, u_bound, l_bound, functions, fidelity_names=None,
                 *, x_opt=None):
        """All fidelity levels and parameters of a multi-fidelity function.

        :param name:           Name of the multi-fidelity function.
        :param u_bound:        Upper bound of the intended input range. Length
                               is also used to determine the (fixed)
                               dimensionality of the function.
        :param l_bound:        Lower bound of the intended input range. Must be
                               of same length as `u_bound`.
        :param functions:      Iterable of function handles for the different
                               fidelities, assumed to be sorted in *descending*
                               order.
        :param fidelity_names: List of names for the fidelities. Must be given
                               to support dictionary- or attribute-style
                               fidelity indexing, such as `f['high']()` and
                               `f.high()`
        :param x_opt:          Location of optimum x_opt for highest fidelity
                               (if known).
        """
        self._name = name

        self.u_bound = np.array(u_bound, dtype=float)
        self.l_bound = np.array(l_bound, dtype=float)
        self._check_bounds()

        if x_opt is not None:
            self.x_opt = np.array(np.atleast_1d(x_opt), dtype=float)
            self._check_x_opt()
        else:
            self.x_opt = x_opt

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
    def name(self):
        return self._name.title()


    @property
    def ndim(self):
        """Dimensionality of the function. Inferred as ``len(self.u_bound)``."""
        return len(self.u_bound)


    @property
    def bounds(self):
        """Lower and upper bounds as a single np.array of shape (2, ndim)."""
        return np.array([self.l_bound, self.u_bound], dtype=float)


    def _check_bounds(self):
        """Perform sanity checks on given bounds"""
        if len(self.u_bound) != len(self.l_bound):
            raise ValueError(f"Length of upper and lower bounds are not equal: "
                             f"{len(self.u_bound)} != {len(self.l_bound)}")

        if not np.all(self.l_bound < self.u_bound):
            indices = np.ravel(np.argwhere(self.u_bound < self.l_bound)).tolist()
            warn(f"Inconsistent bounds at indices {indices}, upper bound not above lower bound.",
                 category=RuntimeWarning)


    def _check_x_opt(self):
        """Perform sanity checks on given `x_opt`"""
        if len(self.x_opt) != self.ndim:
            raise ValueError(f"Length of x_opt and bounds are not equal: "
                             f"{len(self.x_opt)} != {self.ndim}")

        x_opt_in_bounds = np.logical_and(self.l_bound <= self.x_opt,
                                         self.x_opt <= self.u_bound)
        if not np.all(x_opt_in_bounds):
            indices = np.ravel(np.argwhere(~x_opt_in_bounds)).tolist()
            warn(f"x_opt {self.x_opt} out of bounds at indices {indices}",
                 category=RuntimeWarning)


    def __getitem__(self, item):
        if isinstance(item, Integral):
            return self.functions[item]
        elif isinstance(item, str) and self.fidelity_dict:
            return self.fidelity_dict[item]
        else:
            raise IndexError(f"Invalid index '{item}'")


    def __repr__(self):
        return f"MultiFidelityFunction({self.name}, {self.u_bound}, {self.l_bound}, fidelity_names={self.fidelity_names})"


def invert(mff: MultiFidelityFunction) -> MultiFidelityFunction:
    """Invert a MultiFidelityFunction by multiplying all fidelities by -1

    :param mff: The MultiFidelityFunction to invert
    :return:     A new MultiFidelityFunction with the inverted fidelities
    """

    functions = [_invert_function(f) for f in mff.functions]

    return MultiFidelityFunction(
        mff._name, mff.u_bound, mff.l_bound,
        functions,
        fidelity_names=mff.fidelity_names,
        x_opt=mff.x_opt,
    )


def _invert_function(func: Callable) -> Callable:
    """Applies a *-1 modification to the given function"""

    def inverted(x):
        return func(x) * -1

    return inverted
