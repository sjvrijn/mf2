Examples
========

This page contains some examples of typical use of the ``multifidelityfunctions``
package.


Importing
---------

First of all, the import convention for this package is to import it as ``mff``::

    import multifidelityfunctions as mff
    import numpy as np


Fixed Functions
---------------

The majority of multi-fidelity functions in this package are 'fixed' functions.
This means that everything about the function is fixed:

* dimensionality of the input
* number of fidelity levels
* relation between the different fidelity levels

Examples of these functions include the 2D ``mff.booth`` and 8D ``mff.borehole``
functions.

These functions can be directly referenced, and can directly be given one or
more row-vectors to evaluate simultaneously::

    >>> x2 = np.random.random(2)       # single 2D row-vector
    >>> print(mff.booth.high(x2), mff.booth.low(x2))
    ...
    >>> x2 = np.random.random((5, 2))  # 5 row-vectors in 2D
    >>> print(mff.booth.high(x2), mff.booth.low(x2))
    ...
    >>> x8 = np.random.random(8)       # single 8D row-vector
    >>> print(mff.borehole.high(x8), mff.borehole.low(x8))
    ...
    >>> x8 = np.random.random((5, 8))  # 5 row-vectors in 8D
    >>> print(mff.borehole.high(x8), mff.borehole.low(x8))
    ...


Dynamic Dimensionality Functions
--------------------------------

Some functions are dynamic in the dimensionality of the input they accept. An
example of such a function is the ``forrester`` function. The regular 1D
function is included as ``mff.forrester``, but a custom n-dimensional version
can be obtained by calling the factory::

    forrester_4d = mff.Forrester(ndim=4)

This ``forrester_4d`` is then a regular fixed function as seen before.


Adjustable Functions
--------------------

Other functions have a tunable parameter that can be used to adjust the
correlation between the different high and low fidelity levels. For these too,
you can simply call a factory that will return a version of that function with
the parameter fixed to your specification::

    paciorek_high_corr = mff.adjustablepaciorek(a2=0.1)

The exact relationship between the input parameter and resulting correlation
can be found in the documentation of the specific functions.


Adding Your Own MultiFidelityFunction
-------------------------------------

Each function is stored as a ``MultiFidelityFunction``-object, which contains
the dimensionality, intended upper/lower bounds, and of course all fidelity
levels. This class can also be used to define your own multi-fidelity function::

    def sphere_hf(x):
        return x*x

    def sphere_lf(x):
        return abs(x)

    mff_sphere = MultiFidelityFunction(
        name='sphere',
        u_bound=[1],
        l_bound=[-1],
        functions=(sphere_hf, sphere_lf),
        fidelity_names=('high', 'low')
    )

Of these parameters, ``fidelity_names`` is optional, but highly recommended
nonetheless. This package maintains the following naming convention for the
various fidelities:
* 2: 'high', 'low'
* 3: 'high', 'medium', 'low'

