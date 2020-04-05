.. _example_usage:

Example Usage
=============

This example is a reproduction of Figure 1 from http://doi.org/10.1098/rspa.2007.1900 :

The original figure:

.. image:: https://royalsocietypublishing.org/cms/asset/efa57e07-5384-4503-8b2b-ccbe632ffe87/3251fig1.jpg
  :width: 400

Code to reproduce the above figure as close as possible: ::

    # Typical imports: Matplotlib, numpy, sklearn and of course our mf2 package
    import matplotlib.pyplot as plt
    import mf2
    import numpy as np
    from sklearn.gaussian_process import GaussianProcessRegressor as GPR
    from sklearn.gaussian_process import kernels

    # Setting up
    low_x = np.linspace(0,1,11).reshape(-1,1)
    high_x = low_x[[0,4,6,10]]
    diff_x = high_x

    low_y = mf2.forrester.low(low_x)
    high_y = mf2.forrester.high(high_x)
    scale = 1.87  # As reported in the paper
    diff_y = np.array([(mf2.forrester.high(x) - scale*mf2.forrester.low(x))[0]
                       for x in diff_x])

    # Training GP models
    kernel = kernels.ConstantKernel(constant_value=1.0) \
                * kernels.RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0))

    gp_direct = GPR(kernel=kernel).fit(high_x, high_y)
    gp_low = GPR(kernel=kernel).fit(low_x, low_y)
    gp_diff = GPR(kernel=kernel).fit(diff_x, diff_y)

    # Using a lambda function to quickly combine the two models
    co_y = lambda x: scale*gp_low.predict(x) + gp_diff.predict(x)

    # And finally recreating the plot
    plot_x = np.linspace(start=0,stop=1,num=501).reshape(-1,1)
    plt.figure(figsize=(6,5))
    plt.plot(plot_x, mf2.forrester.high(plot_x), linewidth=2, color='black', label='$f_e$')
    plt.plot(plot_x, mf2.forrester.low(plot_x), linewidth=2, color='black', linestyle='--', label='$f_c$')
    plt.scatter(high_x, high_y, marker='o', facecolors='none', color='black', label='$y_e$')
    plt.scatter(low_x, low_y, marker='s', facecolors='none', color='black', label='$y_c$')
    plt.plot(plot_x, gp_direct.predict(plot_x), linewidth=1, color='black', linestyle='--', label='kriging through $y_e$')
    plt.plot(plot_x, co_y(plot_x), linewidth=1, color='black', label='co-kriging')
    plt.xlim([0,1])
    plt.ylim([-10,20])
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.legend(loc=2)
    plt.tight_layout()
    plt.show()

Reproduced figure:

.. image:: ../_static/recreating-forrester-2007.png
  :width: 400
  :alt: Alternative text
