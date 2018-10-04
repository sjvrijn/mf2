from setuptools import setup

with open('README') as f:
    long_description = f.read()

setup(
    name='multifidelityfunctions',
    version='0.0.0',
    description='A collection of analytical benchmark functions in multiple fidelities',
    long_description=long_description,
    author='Sander van Rijn',
    author_email='s.j.van.rijn@liacs.leidenuniv.nl',
    packages=['multifidelityfunctions'],
)
