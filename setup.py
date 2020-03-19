import setuptools
from pathlib import Path

with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='mf2',
    version='2019.11.3',
    description='A collection of analytical benchmark functions in multiple fidelities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sander van Rijn',
    author_email='s.j.van.rijn@liacs.leidenuniv.nl',
    url="https://github.com/sjvrijn/mf2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
