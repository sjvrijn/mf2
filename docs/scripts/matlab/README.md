# Matlab files for scalability comparison

This folder contains the matlab files that were used for the scalability
comparison plots:

 - Utility functions:
 
   - `myscale.m` scales input from [0, 1] to the given new range.

   - `mytiming.m` creates random input of desired size `N` and performs a timing
     experiment akin to Python's [`timeit`].
     
 - Test functions:
 
   - `test_function_output.m` confirms that the matlab code gives the same
     result as the Python code for the same input. Expects input
     `input_<N>d.mat` and output `output_<N>d_<Name>_<Fidelity>.mat`-files to
     be available. These can be created using [`scipy.io.savemat`] in Python.

   - `test_function_performance.m` calls `mytiming.m` for all listed
     function-fidelity combinations, with increasing evaluation sizes `N`. By
     default, values for `N` are successive powers of 10: 10^0 -- 10^6.
     
 - Matlab implementations of benchmark functions

   The following implementations were retrieved from
   ``https://www.sfu.ca/~ssurjano/multi.html`` on 2017-10-02, and are available
   here under their original GNU GPL v2.0 licenses:
   
   - [Borehole]: `borehole.m` & `boreholelc.m`

   - [Currin]: `curretal88exp.m` & `curretal88explc.m`

   - [Park91a]: `park91a.m` & `park91alc.m`

   - [Park91b]: `park91b.m` & `park91blc.m`


[`timeit`]: https://docs.python.org/3/library/timeit.html#timeit.Timer.autorange
[`scipy.io.savemat`]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.savemat.html#scipy.io.savemat
[Borehole]: https://www.sfu.ca/~ssurjano/borehole.html
[Currin]: https://www.sfu.ca/~ssurjano/curretal88exp.html
[Park91a]: https://www.sfu.ca/~ssurjano/park91a.html
[Park91b]: https://www.sfu.ca/~ssurjano/park91b.html
