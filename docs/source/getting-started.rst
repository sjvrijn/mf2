.. _getting_started:

Getting Started
===============

This page contains some explained examples to help get you started with using
the ``mf2`` package.

The Basics: What's in a MultiFidelityFunction?
----------------------------------------------

This package serves as a collection of functions with multiple fidelity levels.
The number of levels is at least two, but differs by function. Each function is
encoded as a :class:`~mf2.multi_fidelity_function.MultiFidelityFunction`
with the following attributes:

``.name``
    The *name* is simply a standardized format of the name as an attribute to
    help identify which function is being represented [#footnote_name]_ .

``.ndim``
    Number of dimensions. This is the dimensionality (i.e. length) of the input
    vector X of which the objective is evaluated.

``.fidelity_names``
    This is a list of the human-readable names given to each fidelity.

``.u_bound``, ``.l_bound``
    The upper and lower bounds of the search-space for the function.

``.functions``
    A list of the actual function references. You won't typically need this
    list though, as will be explained next in :ref:`accessing_functions`.



Simple Usage
------------

.. _accessing_functions:

Accessing the functions
^^^^^^^^^^^^^^^^^^^^^^^

As an example, we'll use the :mod:`~mf2.booth` function. As we can see using
``.ndim`` and the bounds, it is two-dimensional:

    >>> from mf2 import booth
    >>> print(booth.ndim)
    2
    >>> print(booth.l_bound, booth.u_bound)
    [-10. -10.] [10. 10.]

Most multi-fidelity functions in ``mf2`` are *bi-fidelity* functions, but a
function can have any number of fidelities. A bi-fidelity function has two
fidelity levels, which are typically called ``high`` and ``low``. You can
easily check the names of the fidelities by printing the ``fidelity_names``
attribute of a function:

    >>> print(len(booth.fidelity_names))
    2
    >>> print(booth.fidelity_names)
    ['high', 'low']

These are just the names of the fidelities. The functions they represent can be
accessed as an object-style *attribute*,

    >>> print(booth.high)
    <function booth_hf at 0x...>

as a dictionary-style *key*,

    >>> print(booth['low'])
    <function booth_lf at 0x...>

or with a list-style *index* (which just passes through to ``.functions``).

    >>> print(booth[0])
    <function booth_hf at 0x...>
    >>> print(booth[0] is booth.functions[0])
    True

The object-style notation ``function.fidelity()`` is recommended for explicit
access, but the other notations are available for more dynamic usage. With the
list-style access, the *highest* fidelity is always at index *0*.


Calling the functions
^^^^^^^^^^^^^^^^^^^^^

All functions in the ``mf2`` package assume *row-vectors* as input. To evaluate
the function at a  single point, it can be given as a simple Python list or 1D
numpy array. Multiple points can be passed to the function individually, or
combined into a 2D list/array. The output of the function will always be
returned as a 1D numpy array:

    >>> X1 = [0.0, 0.0]
    >>> print(booth.high(X1))
    [74.]
    >>> X2 = [
    ...     [ 1.0,  1.0],
    ...     [ 1.0, -1.0],
    ...     [-1.0,  1.0],
    ...     [-1.0, -1.0]
    ... ]
    >>> print(booth.high(X2))
    [ 20.  80.  72. 164.]


Using the bounds
^^^^^^^^^^^^^^^^

Each function also has a given upper and lower bound, stored as a 1D numpy
array. They will be of the same length, and exactly as long as the
dimensionality of the function [#footnote_ndim]_ .

Below is an example function to create a uniform sample within the bounds::

    import numpy as np

    def sample_in_bounds(func, n_samples):
        raw_sample = np.random.random((n_samples, func.ndim))

        scale = func.u_bound - func.l_bound
        sample = (raw_sample * scale) + func.l_bound

        return sample


Kinds of functions
------------------

Fixed Functions
^^^^^^^^^^^^^^^

The majority of multi-fidelity functions in this package are 'fixed' functions.
This means that everything about the function is fixed:

* dimensionality of the input
* number of fidelity levels
* relation between the different fidelity levels

Examples of these functions include the 2D :mod:`~mf2.booth` and 8D
:mod:`~mf2.borehole` functions.


Dynamic Dimensionality Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some functions are dynamic in the dimensionality of the input they accept. An
example of such a function is the ``forrester`` function. The regular 1D
function is included as ``mf2.forrester``, but a custom n-dimensional version
can be obtained by calling the factory::

    forrester_4d = mf2.Forrester(ndim=4)

This ``forrester_4d`` is then a regular fixed function as seen before.


Adjustable Functions
^^^^^^^^^^^^^^^^^^^^

Other functions have a tunable parameter that can be used to adjust the
correlation between the different high and low fidelity levels. For these too,
you can simply call a factory that will return a version of that function with
the parameter fixed to your specification::

    paciorek_high_corr = mf2.adjustable.paciorek(a2=0.1)

The exact relationship between the input parameter and resulting correlation
can be found in the documentation of the specific functions. See for example
:mod:`~mf2.adjustable.paciorek`.

Adding Your Own
---------------

Each function is stored as a ``MultiFidelityFunction``-object, which contains
the dimensionality, intended upper/lower bounds, and of course all fidelity
levels. This class can also be used to define your own multi-fidelity function.

To do so, first define regular functions for each fidelity. Then create the
``MultiFidelityFunction`` object by passing a name, the upper and lower bounds,
and a tuple of the functions for the fidelities.

The following is an example for a 1-dimensional multi-fidelity function named
``my_mf_sphere`` with three fidelities::

    import numpy as np
    from mf2 import MultiFidelityFunction

    def sphere_hf(x):
        return x*x

    def sphere_mf(x):
        return x * np.sqrt(x) * np.sign(x)

    def sphere_lf(x):
        return np.abs(x)

    my_mf_sphere = MultiFidelityFunction(
        name='sphere',
        u_bound=[1],
        l_bound=[-1],
        functions=(sphere_hf, sphere_mf, sphere_lf),
    )

These functions can be accessed using list-style *indices*, but as no names
are given, the object-style *attributes* or dict-style *keys* won't work:

    >>> print(my_mf_sphere[0])
    <function sphere_hf at 0x...>
    >>> print(my_mf_sphere['medium'])
    ---------------------------------------------------------------------------
    IndexError                                Traceback (most recent call last)
    ...
    IndexError: Invalid index 'medium'
    >>> print(my_mf_sphere.low)
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    ...
    AttributeError: 'MultiFidelityFunction' object has no attribute 'low'
    >>> print(my_mf_sphere.fidelity_names)
    None

To enable access by attribute or key, a tuple containing a name for each fidelity
is required. Let's extend the previous example by adding
``fidelity_names=('high', 'medium', 'low')``::

    my_named_mf_sphere = MultiFidelityFunction(
        name='sphere',
        u_bound=[1],
        l_bound=[-1],
        functions=(sphere_hf, sphere_mf, sphere_lf),
        fidelity_names=('high', 'medium', 'low'),
    )

Now we the attribute and key access will work:

    >>> print(my_named_mf_sphere[0])
    <function sphere_hf at 0x...>
    >>> print(my_named_mf_sphere['medium'])
    <function sphere_mf at 0x...>
    >>> print(my_named_mf_sphere.low)
    <function sphere_lf at 0x...>
    >>> print(my_named_mf_sphere.fidelity_names)
    ('high', 'medium', 'low')




.. rubric:: Footnotes

.. [#footnote_name] This is as they're instances of MultiFidelityFunction instead
                    of separate classes.

.. [#footnote_ndim] In fact, ``.ndim`` is defined as ``len(self.u_bound)``
