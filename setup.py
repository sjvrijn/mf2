import setuptools

with open('README.md') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('requirements-dev.txt') as f:
    requirements_dev = f.read().splitlines()

setuptools.setup(
    name='mf2',
    version='2022.06.0',
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={"dev": requirements_dev},
)
