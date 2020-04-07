---
title: 'MF2: A Collection of Multi-Fidelity Benchmark Functions in Python'
tags:
  - Python
  - optimization
  - benchmarks
authors:
  - name: Sander van Rijn
    orcid: 0000-0001-6159-041X
    affiliation: 1
  - name: Sebastian Schmitt
    affiliation: 2
affiliations:
  - name: Leiden University, The Netherlands
    index: 1
  - name: Honda Research Institute Europe, Germany
    index: 2
date: 7 April 2020
bibliography: paper.bib

---


# Summary

The field of (evolutionary) optimization algorithms often works with expensive
black-box optimization problems. However, for the development of novel
algorithms and approaches, real-world problems are not feasible due to their
high computational cost. Instead, benchmark functions such as Sphere, Rastrigin,
and Ackley are typically used. These functions are not only fast to compute, but
also have known properties which are very helpful when examining the performance
of new algorithms.

As only a limited set of benchmark functions are typically used in literature,
compiling a set of implementations for the most commonly used functions is
warranted. This ensures correctness of the functions, makes any results directly
comparable, and simply saves time from not having to implement the functions
yourself. An example of a commonly used benchmark suite for optimizing
continuous problems is the COCO BBOB software by @nikolaus_hansen:2019.

As simulation-based problems in engineering are requiring increasingly more time
and computation power, a new sub-field of *multi-fidelity* optimization has
gained popularity. A multi-fidelity problem is characterised by having multiple
versions of an evaluation function that differ in their accuracy of describing
the real objective. A real-world example would be the aerodynamic efficiency of
an airfoil: A *low-fidelity* simulation would use a coarse mesh, and give lower
accuracy, but be fast to calculate, while a *high-fidelity* simulation would use
a much finer mesh and therefore be more accurate while taking longer to
calculate. Multi-fidelity methods aim to combine these multiple information
sources to obtain better results in equal or less time compared to only using a
single information source.

Because multi-fidelity problems are a new class of problems, the existing
single-fidelity benchmark suites that exist cannot be used for this field. To
this end, new multi-fidelity benchmark functions have been introduced in the
literature and are being adopted by other researchers.

This new class of benchmark problems is best served by introducing
a new implementation suite because their structure is inherently different from
other benchmarks. That is, multi-fidelity problems naturally benefit from
having the different fidelities combined into a single 'problem'. No existing
suite of benchmark functions currently uses such a structure, or can easily
accomodate it. A new suite additionally gives more freedom to adapt to new
multi-fidelity benchmarks as the field continues to evolve and new needs become
apparent.

The ``MF2`` package provides a consistent Python implementation of a collection
of these Multi-Fidelity Functions. It uses a standard interface that allows for
querying single vectors or multiple row-vectors as a single matrix. It also
offers a simple factory pattern interface for functions with parameters for e.g.
correlation and dimensionality. A plot of how these implementations scale can
be seen in \autoref{fig:scalability}.

At this moment, ``MF2`` has collected functions
from the following previous works:

  * @forrester:2007 introduced a simple 1D bi-fidelity function for mostly
    illustrative purposes.
  * @simulationlib:2017 have previously collected a small collection of
    MATLAB/R implementations for the Borehole, Currin and Park91 A and B
    functions.
  * @dong_multi-fidelity:2015 introduced bi-fidelity versions of the
    Bohachevsky, Booth, Branin, Himmelblau and Six-hump Camelback functions.
  * @toal_considerations:2015 introduced correlation-adjustable multi-fidelity
    versions of the Branin, Paciorek, Hartmann3 and Trid functions.

This package is currently in use by the authors in their research on multi-
fidelity hierarchical surrogate models.

![**Scalability plot** This plot shows how the evaluation time of high- and
low-fidelity functions scales with the number of points *N* being passed in
simultaneously. The times are divided by the time needed for N=1 as a
normalization. Results are grouped by function dimensionality. If there are
multiple functions, the mean is plotted with error bars indicating the minimum
and maximum time. Note that the 6D Hartmann6 function is significantly more
computationally expensive than other functions by definition, as it requires
multiple matrix multiplications.\label{fig:scalability}](scalability.pdf)

# Acknowledgements

This work is part of the research program DAMIOSO with project number
628.006.002, which is partly financed by the Netherlands Organisation
for Scientific Research (NWO).

The first author would like to thank dr. Matthijs van Leeuwen, prof. dr. Thomas
Bäck, and dr. Markus Olhofer for their supervision and involvement in the
DAMIOSO project.

# References