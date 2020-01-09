.. Multi-Fidelity Functions documentation master file, created by
   sphinx-quickstart on Thu Nov 14 00:14:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MF2: Multi-Fidelity Functions
=============================

This is the documentation for the ``mf2`` package. For a short introduction with
examples, have a look at the :ref:`getting_started` page. Otherwise, you can
look at the available functions in the package by category.

This package contains Python implementations for a variety of multi-fidelity
benchmark functions typically used in numerical optimization research.

A multi-fidelity function usually reprensents an objective which should be
optimized. The term 'multi-fidelity' refers to the fact, that multiple versions
of the objective function exist which differ in the accuray to describe the
real objective. A typical real-world example would be the aerodynamic
efficiency of an airfoil, e.g., its drag value for a given lift value. The
different fidelity levels are given by the accuracy of the evaluation method
used to estimate the efficiency. Lower-fidelity versions of the objective
function refer to less accurate, but simpler approximations of the objective,
such as computational fluid dynamic simulations on rather coarse meshes,
whereas higher fidelity levels refer to more accurate but also much more
demaning evaluations such as prototype tests in wind tunnels. The hope of
multi-fildelity optimization approaches is that many of the not-so-accurate but
simple low-fidelity evaluations can be uaws to achieve improved results on the
realistic high-fidelity version of the objective where only very few
evaluations can be performed.

The only dependency of the mf2 package is the `numpy` (https://numpy.org/)
package.


Last updated: (|today|)


Contents
========

.. toctree::
   :maxdepth: 2

   install
   getting-started
   mf2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
