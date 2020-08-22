Installation
============

The recommended way to install `mf2` is with Python's `pip`::

    python3 -m pip install --user mf2

or alternatively using `conda`::

    conda install -c conda-forge mf2


For the latest version, you can install directly from source::

    python3 -m pip install --user https://github.com/sjvrijn/mf2/archive/master.zip


To work in your own version locally, it is best to clone the repository first::

    git clone https://github.com/sjvrijn/mf2.git
    cd mf2
    python3 -m pip install --user -e .[dev]
