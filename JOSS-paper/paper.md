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
date: 31 December 2019
bibliography: paper.bib


# Summary

The field of (evolutionary) optimization algorithms often works with expensive
black-box optimization problems. Because of how computationally expensive they
are, real-world problems are not a first choice to test on when developing new
algorithms. Instead, benchmark functions such as Sphere, Rastrigin, and Ackley
are used. These functions are not only fast to compute, but also have known
landscape properties that can be taken into account when examining the
performance of new algorithms.

As the same sets of benchmark functions are typically used in literature, having
it makes sense to simply use a pre-written implementation. This ensures
correctness of the functions, makes any results directly comparable, and simply
saves time from not having to implement the functions yourself. For the
'regular' single-fidelity benchmarks, the COCO BBOB
[@nikolaus_hansen:2019] software is such a widely used collection.

As the field of *multi-fidelity* optimization is becoming more popular, a
similar set of common benchmarks is appearing in the literature: Dong et al.
[@dong_multi-fidelity:2015] introduced bi-fidelity versions of the Bohachevsky,
Booth, Branin, Himmelblau and Six-hump Camelback functions. Toal
[@toal_considerations:2015] introduced correlation-adjustable multi-fidelity
versions of the Branin, Paciorek, Hartmann3 and Trid functions. Surjanovic and
Bingham [@simulationlib:2017] have previously collected a small collection of
MATLAB/R implementations for the Borehole, Currin and Park91 A and B functions.

``MF2`` is a new collection of these commonly used multi-fidelity functions,
implemented in Python. It uses a standard interface that allows for querying
single vectors or multiple row-vectors as a single matrix. It also offers a
simple factory pattern interface for functions with parameters for e.g.
correlation and dimensionality.

# Acknowledgements

This work is part of the research program DAMIOSO with project number
628.006.002, which is partly financed by the Netherlands Organisation
for Scientific Research (NWO).

# References