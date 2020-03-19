#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
create_regression_data.py: helper script to create data for regression tests.

Performs 2 steps for each function that is tested in 'regression_test.py':
 * If no existing input-files are found:
   - Creates standardized input for required dimensionalities
   - Stores them as 'regression_files/input{ndim}d.npy'.
 * If no existing output-files are found:
   - Loads the corresponding input-file
   - Rescales the input to within the boundaries of the function
   - Calculates the output of the functions at the rescaled input
   - Stores the output as
     'regression_files/output_{ndim}d_{func.name}_{fidelity}.npy'
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'

import numpy as np
from pyprojroot import here

from utils import rescale, ValueRange
from regression_test import _functions_to_test


def create_and_store_input(ndim):
    fname = here(f'tests/regression_files/input_{ndim}d.npy')
    if not fname.exists():
        np.random.seed(20160501)  # Setting seed for reproducibility
        np.save(fname, np.random.rand(100,ndim))
        print(f"input {ndim}d created")


def create_and_store_output(func, fidelity):
    file_out = here(f'tests/regression_files/output_{func.ndim}d_{func.name}_{fidelity}.npy')
    if file_out.exists():
        return

    file_in = here(f'tests/regression_files/input_{func.ndim}d.npy')
    if not file_in.exists():
        create_and_store_input(func.ndim)

    x = rescale(np.load(file_in),
                range_in=ValueRange(0,1),
                range_out=ValueRange(*func.bounds))
    np.save(file_out, func[fidelity](x))
    print(f"output {func.ndim}d {func.name} created")


if __name__ == '__main__':
    for func in _functions_to_test:
        for fid in func.fidelity_names:
            create_and_store_output(func, fid)
