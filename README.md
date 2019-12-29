[![PyPI version](https://badge.fury.io/py/mf2.svg)](https://badge.fury.io/py/mf2)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mf2)
[![Build Status](https://travis-ci.org/sjvrijn/mf2.svg?branch=master)](https://travis-ci.org/sjvrijn/mf2)
[![Coverage Status](https://coveralls.io/repos/github/sjvrijn/mf2/badge.svg?branch=master)](https://coveralls.io/github/sjvrijn/mf2?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/54144e7d406b4558a14996b06a89adf8)](https://www.codacy.com/manual/sjvrijn/mf2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sjvrijn/mf2&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/mf2/badge/?version=latest)][docs-badge]
[![Gitter](https://badges.gitter.im/pymf2/community.svg)][gitter-badge]

# Multi-Fidelity-Functions

This package contains Python implementations for a variety of multi-fidelity
benchmark functions. The only dependency is the `numpy` package.


## Installation

The recommended way to install `mf2` is with Python's Pip:
```
python3 -m pip install --user mf2
```

For the latest version, you can install directly from source:
```
python3 -m pip install --user https://github.com/sjvrijn/mf2/archive/master.zip
```

To work in your own version locally, it is best to clone the repository first:
```
git clone https://github.com/sjvrijn/mf2.git
cd mf2
python3 -m pip install --user -e .
```

## Example Usage

```python
import mf2
import numpy as np

forrester = mf2.Forrester(ndim=2)
np.random.seed(42)
X = np.random.random((5, 2))  # 5 samples in 2D

print(forrester.high(X))
# Out: array([ 6.20598519, -2.90702413, -0.96082789,  0.78490341, -2.56183228])

print(forrester.low(X))
# Out: array([6.47672047, 1.89322581, 7.95952025, 5.77115291, 2.17314591])
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
    * add the function in the `tests/property_test.py` and
    `tests/regression_test.py` files
    * run the `tests/create_regression_data.py` file to generate the new data
    files
    * run the tests
3. Make sure to commit all new and updated files to git (Travis-CI will complain
otherwise ;)
4. Create a pull-request!

If you need any help with this process, please get in touch as outlined under
**Contact**.

## Contact

The [Gitter][gitter] channel is the preferred way to get in touch for any other
questions, comments or discussions about this package.




[docs]:         https://mf2.readthedocs.io/en/latest/
[docs-badge]:   https://mf2.readthedocs.io/en/latest/?badge=latest
[gitter]:       https://gitter.im/pymf2/community
[gitter-badge]: https://gitter.im/pymf2/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[new-issue]:    https://github.com/sjvrijn/mf2/issues/new
