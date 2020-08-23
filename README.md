# Multi-Fidelity-Functions

| Package Info | Status | Support |
|--------------|--------|---------|
| [![PyPI version](https://badge.fury.io/py/mf2.svg)](https://badge.fury.io/py/mf2) | [![Build Status](https://travis-ci.com/sjvrijn/mf2.svg?branch=master)](https://travis-ci.com/sjvrijn/mf2) | [![Documentation Status](https://readthedocs.org/projects/mf2/badge/?version=latest)][docs-badge] |
| [![Conda](https://img.shields.io/conda/v/conda-forge/mf2)](https://anaconda.org/conda-forge/mf2) | [![Coverage Status](https://coveralls.io/repos/github/sjvrijn/mf2/badge.svg?branch=master)](https://coveralls.io/github/sjvrijn/mf2?branch=master) | [![Gitter](https://badges.gitter.im/pymf2/community.svg)][gitter-badge] |
| ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mf2) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/54144e7d406b4558a14996b06a89adf8)](https://www.codacy.com/manual/sjvrijn/mf2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sjvrijn/mf2&amp;utm_campaign=Badge_Grade) | |
| [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) | [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) | |
| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3749395.svg)](https://doi.org/10.5281/zenodo.3749395) | [![status](https://joss.theoj.org/papers/2575e93fc693c5c3bfa8736c60c35398/status.svg)](https://joss.theoj.org/papers/2575e93fc693c5c3bfa8736c60c35398) | |

## Introduction

The `mf2` package providing consistent, efficient and tested Python
implementations of a variety of multi-fidelity benchmark functions. The goal is
to simplify life for numerical optimization researchers by saving time otherwise
spent reimplementing and debugging the same common functions, and enabling
direct comparisons with other work using the same definitions, improving
reproducibility in general.

A multi-fidelity function usually reprensents an objective which should be
optimized. The term 'multi-fidelity' refers to the fact that multiple versions
of the objective function exist, which differ in the accuracy to describe the
real objective. A typical real-world example would be the aerodynamic
efficiency of an airfoil, e.g., its drag value for a given lift value. The
different fidelity levels are given by the accuracy of the evaluation method
used to estimate the efficiency. Lower-fidelity versions of the objective
function refer to less accurate, but simpler approximations of the objective,
such as computational fluid dynamic simulations on rather coarse meshes,
whereas higher fidelity levels refer to more accurate but also much more
demanding evaluations such as prototype tests in wind tunnels. The hope of
multi-fildelity optimization approaches is that many of the not-so-accurate but
simple low-fidelity evaluations can be used to achieve improved results on the
realistic high-fidelity version of the objective where only very few
evaluations can be performed.

The only dependency of the mf2 package is the `numpy` package.

Documentation is available at [mf2.readthedocs.io][docs]

## Installation

The recommended way to install `mf2` is with Python's `pip`:
```
python3 -m pip install --user mf2
```
or alternatively using `conda`:
```
conda install -c conda-forge mf2
```

For the latest version, you can install directly from source:
```
python3 -m pip install --user https://github.com/sjvrijn/mf2/archive/master.zip
```

To work in your own version locally, it is best to clone the repository first,
and additionally install the dev-requirements:
```
git clone https://github.com/sjvrijn/mf2.git
cd mf2
python3 -m pip install --user -e .[dev]
```

## Example Usage

```python
import mf2
import numpy as np

# set numpy random seed for reproducibility
np.random.seed(42)
# generate 5 random samples in 2D as matrix
X = np.random.random((5, 2))

# print high fidelity function values
print(mf2.branin.high(X))
# Out: array([36.78994906 34.3332972  50.48149005 43.0569396  35.5268224 ])

# print low fidelity function values
print(mf2.branin.low(X))
# Out: array([-5.8762639  -6.66852889  3.84944507 -1.56314141 -6.23242223])
```

For more usage examples, please refer to the full documentation on
[readthedocs][docs].

## Contributing

Contributions to this project are more than welcome!

### Bugs
If you've found a problem of some sort, please open an issue on
[GitHub][new-issue].

### Additions
To add new functions to this package, you can roughly follow the following
steps:

1. Implement the function in a new file in the appropriate (sub)folder
2. Add it to the tests:
   * Add the function in the `tests/property_test.py` and
   `tests/regression_test.py` files
   * Run the tests: `pytest tests`. It will fail the first time while the
   [`pytest-regressions`][pytest-regressions] package automatically creates
   the new output files.
   * Run the tests again to confirm that all tests now pass.
3. Make sure to commit all new and updated files to git (Travis-CI will
complain otherwise ;)
4. Create a pull-request!

If you need any help with this process, please get in touch as outlined under
**Contact**.

## Contact

The [Gitter][gitter] channel is the preferred way to get in touch for any other
questions, comments or discussions about this package.

[docs]:               https://mf2.readthedocs.io/en/latest/
[docs-badge]:         https://mf2.readthedocs.io/en/latest/?badge=latest
[gitter]:             https://gitter.im/pymf2/community
[gitter-badge]:       https://gitter.im/pymf2/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[new-issue]:          https://github.com/sjvrijn/mf2/issues/new
[pytest-regressions]: https://github.com/ESSS/pytest-regressions
