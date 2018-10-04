#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

"""
artificialMultifidelity.py:

This function is a based on a set of equations with one-dimensional
input and output. The lowest fidelity is 1, while 6 is the highest
fidelity available. Exact formulas as given in the original paper by
J. Branke et al. are listed below. For input in more than one dimension,
the sum over all values as calculated for each dimension is returned. Note
that the location of the global optimum shifts from the right for fidelities
1-2, to equal for fidelities 3-4 and finally to the left for fidelities 5-6.
This is on purpose to simulate the occurrence of local optima in lower
fidelity evaluations.

Below are the exact formulas for all 6 fidelity levels.

\f{eqnarray*{ \\
f1(x) =& \min \{ &
         (x-2)^2,\\
      && (x+2)^2 + 2 \} \\

f2(x) =& \min \{ &
         (x-2)^2 + 5\sin ( \frac{\pi}{2} (x+1)),\\
      && (x+2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + \frac{6}{5} \} \\

f3(x) =& \min \{ &
         (x-2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )),\\
      && (x+2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        \frac{2}{5} \} \\

f4(x) =& \min \{ &
        (x-2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )),\\
     && (x+2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )) - \frac{2}{5} \} \\

f5(x) =& \min \{ &
        (x-2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )) + 2\sin ( 4\pi (x + \frac{15}{8} )), \\
     && (x+2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )) + 2\sin ( 4\pi (x + \frac{15}{8} )) -
        \frac{6}{5} \} \\

f6(x) =& \min \{ &
        (x-2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )) + 2\sin ( 4\pi (x + \frac{15}{8} )) + \sin ( 8\pi (x+2)), \\
     && (x+2)^2 + 5\sin ( \frac{\pi}{2} (x+1)) + 4\sin ( \pi (x + \frac{3}{2} )) +
        3\sin ( 2\pi (x + \frac{7}{4} )) + 2\sin ( 4\pi (x + \frac{15}{8} )) +
        \sin ( 8\pi (x+2))- 2 \} \\
 \f}

References:

[Efficient Use of Partially Converged Simulations in Evolutionary Optimization, J. Branke et al. 2016.]
(http://ieeexplore.ieee.org/document/7469882/)

([Public full text PDF](http://wrap.warwick.ac.uk/79047/7/WRAP_CFD_TEC_merged_final.pdf))
"""

__author__ = 'Sander van Rijn'
__email__ = 's.j.van.rijn@liacs.leidenuniv.nl'


def evaluateFidelity1(inputs):
    total = 0
    for x in inputs:
        s1 = (x - 2) * (x - 2)
        s2 = (x + 2) * (x + 2) + 2
        total += min(s1, s2)
    return total


def evaluateFidelity2(inputs):
    total = 0
    for x in inputs:
        equal_part = 5 * math.sin((math.pi / 2) * (x + 1))
        s1 = (x - 2) * (x - 2) + equal_part
        s2 = (x + 2) * (x + 2) + equal_part + 6 / 5
        total += min(s1, s2)
    return total


def evaluateFidelity3(inputs):
    total = 0
    for x in inputs:
        equal_part = 5 * math.sin((math.pi / 2) * (x + 1)) \
                     + 4 * math.sin(math.pi * (x + 3 / 2))
        s1 = (x - 2) * (x - 2) + equal_part
        s2 = (x + 2) * (x + 2) + equal_part + 2 / 5
        total += min(s1, s2)
    return total


def evaluateFidelity4(inputs):
    total = 0
    for x in inputs:
        equal_part = 5 * math.sin((math.pi / 2) * (x + 1)) \
                     + 4 * math.sin(math.pi * (x + 3 / 2)) \
                     + 3 * math.sin(2 * math.pi * (x + (7 / 4)))
        s1 = (x - 2) * (x - 2) + equal_part
        s2 = (x + 2) * (x + 2) + equal_part - 2 / 5
        total += min(s1, s2)
    return total


def evaluateFidelity5(inputs):
    total = 0
    for x in inputs:
        equal_part = 5 * math.sin((math.pi / 2) * (x + 1)) \
                     + 4 * math.sin(math.pi * (x + 3 / 2)) \
                     + 3 * math.sin(2 * math.pi * (x + (7 / 4))) \
                     + 2 * math.sin(4 * math.pi * (x + (15 / 8)))
        s1 = (x - 2) * (x - 2) + equal_part
        s2 = (x + 2) * (x + 2) + equal_part - 6 / 5
        total += min(s1, s2)
    return total


def evaluateFidelity6(inputs):
    total = 0
    for x in inputs:
        equal_part = 5 * math.sin((math.pi / 2) * (x + 1)) \
                     + 4 * math.sin(math.pi * (x + 3 / 2)) \
                     + 3 * math.sin(2 * math.pi * (x + (7 / 4))) \
                     + 2 * math.sin(4 * math.pi * (x + (15 / 8))) \
                     + math.sin(8 * math.pi * (x + 2))
        s1 = (x - 2) * (x - 2) + equal_part
        s2 = (x + 2) * (x + 2) + equal_part - 2
        total += min(s1, s2)
    return total


def artificial_multifidelity(fidelity, inputs):
    if fidelity == 1:
        return evaluateFidelity1(inputs)
    elif fidelity == 2:
        return evaluateFidelity2(inputs)
    elif fidelity == 3:
        return evaluateFidelity3(inputs)
    elif fidelity == 4:
        return evaluateFidelity4(inputs)
    elif fidelity == 5:
        return evaluateFidelity5(inputs)
    elif fidelity == 6:
        return evaluateFidelity6(inputs)
    else:
        raise ValueError("Argument 'fidelity' must be an integer between [1-6], was {}".format(fidelity))
