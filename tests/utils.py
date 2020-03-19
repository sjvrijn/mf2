# -*- coding: utf-8 -*-

"""
utils.py: collection of utilities for testing the mf2 package
"""


from collections import namedtuple
import numpy as np


ValueRange = namedtuple('ValueRange', ['min', 'max'])

def determinerange(values):
    """Determine the range of values in each dimension"""
    r = ValueRange(np.min(values, axis=0), np.max(values, axis=0))
    if np.any(r.max - r.min < 1e-8):
        r = ValueRange(r.min - 1e8, r.max + 1e8)
    return r


def rescale(values, *, range_in=None, range_out=ValueRange(0, 1), scale_only=False):
    """Perform a scale transformation of `values`: [range_in] --> [range_out]"""

    if range_in is None:
        range_in = determinerange(values)
    elif not isinstance(range_in, ValueRange):
        range_in = ValueRange(*range_in)

    if not isinstance(range_out, ValueRange):
        range_out = ValueRange(*range_out)

    scale_out = range_out.max - range_out.min
    scale_in = range_in.max - range_in.min

    if scale_only:
        scaled_values = (values / scale_in) * scale_out
    else:
        scaled_values = (values - range_in.min) / scale_in
        scaled_values = (scaled_values * scale_out) + range_out.min

    return scaled_values
