# MF2: Multi-Fidelity-Functions

| Package Info                                 | Status                                                | Support                            |
|----------------------------------------------|-------------------------------------------------------|------------------------------------|
| [![PyPI version][PyPI-badge]][PyPI-url]      | [![Tests status][tests-badge]][actions-page]          | [![Docs Status][docs-badge]][docs] |
| [![Conda][conda-badge]][conda-url]           | [![Coverage Status][coveralls-badge]][coveralls]      | [![Gitter][gitter-badge]][gitter]  |
| ![PyPI - Python Version][PyPI-python-badge]  | [![Codacy Badge][codacy-badge]][codacy-url]           |                                    |
| [![License: GPL v3][license-badge]][license] | [![Project Status: Active][devstate-badge]][devstate] |                                    |
| [![DOI][Zenodo-badge]][Zenodo-url]           | [![CII Best Practices][cii-badge]][cii-url]           |                                    |
| [![status][JOSS-badge]][JOSS paper]          |                                                       |                                    |

## Introduction

The `mf2` package provides consistent, efficient and tested Python
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

The recommended way to install `mf2` in your (virtual) environment is with
Python's `pip`:
```
pip install mf2
```
or alternatively using `conda`:
```
conda install -c conda-forge mf2
```

For the latest version, you can install directly from source:
```
pip install https://github.com/sjvrijn/mf2/archive/main.zip
```

To work in your own version locally, it is best to clone the repository first,
and additionally create an editable install that includes the dev-requirements:
```
git clone https://github.com/sjvrijn/mf2.git
cd mf2
pip install -e ".[dev]"
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

Contributions to this project such as bug reports or benchmark function
suggestions are more than welcome! Please refer to
[``CONTRIBUTING.md``][CONTRIBUTING.md] for more details.

## Contact

The [Gitter][gitter] channel is the preferred way to get in touch for any other
questions, comments or discussions about this package.

## Citation

Was this package useful to you? Great! If this leads to a publication, we'd
appreciate it if you would cite our [JOSS paper]:

```
@article{vanRijn2020,
  doi = {10.21105/joss.02049},
  url = {https://doi.org/10.21105/joss.02049},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {52},
  pages = {2049},
  author = {Sander van Rijn and Sebastian Schmitt},
  title = {MF2: A Collection of Multi-Fidelity Benchmark Functions in Python},
  journal = {Journal of Open Source Software}
}
```

[PyPI-url]:             https://badge.fury.io/py/mf2
[conda-url]:            https://anaconda.org/conda-forge/mf2
[license]:              https://www.gnu.org/licenses/gpl-3.0
[Zenodo-url]:           https://doi.org/10.5281/zenodo.4540752
[JOSS paper]:           https://joss.theoj.org/papers/10.21105/joss.02049

[actions-page]:         https://github.com/sjvrijn/mf2/actions
[coveralls]:            https://coveralls.io/github/sjvrijn/mf2?branch=main
[codacy-url]:           https://www.codacy.com/manual/sjvrijn/mf2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sjvrijn/mf2&amp;utm_campaign=Badge_Grade
[devstate]:             https://www.repostatus.org/#active
[cii-url]:              https://bestpractices.coreinfrastructure.org/projects/4231

[docs]:                 https://mf2.readthedocs.io/en/latest/?badge=latest
[gitter]:               https://gitter.im/pymf2/community

[CONTRIBUTING.md]:      https://github.com/sjvrijn/mf2/blob/master/CONTRIBUTING.md

[PyPI-badge]:           https://badge.fury.io/py/mf2.svg
[conda-badge]:          https://img.shields.io/conda/v/conda-forge/mf2
[PyPI-python-badge]:    https://img.shields.io/pypi/pyversions/mf2
[license-badge]:        https://img.shields.io/badge/License-GPLv3-blue.svg
[Zenodo-badge]:         https://zenodo.org/badge/DOI/10.5281/zenodo.4540752.svg
[JOSS-badge]:           https://joss.theoj.org/papers/10.21105/joss.02049/status.svg
[tests-badge]:          https://github.com/sjvrijn/mf2/workflows/tests/badge.svg
[coveralls-badge]:      https://coveralls.io/repos/github/sjvrijn/mf2/badge.svg?branch=main
[codacy-badge]:         https://api.codacy.com/project/badge/Grade/54144e7d406b4558a14996b06a89adf8
[devstate-badge]:       https://www.repostatus.org/badges/latest/active.svg
[cii-badge]:            https://bestpractices.coreinfrastructure.org/projects/4231/badge
[docs-badge]:           https://readthedocs.org/projects/mf2/badge/?version=latest
[gitter-badge]:         https://badges.gitter.im/pymf2/community.svg
