from setuptools import setup
import multifidelityfunctions

with open('README') as f:
    long_description = f.read()

setup(
    name='multifidelityfunctions',
    version=multifidelityfunctions.__version__,
    description='A collection of analytical benchmark functions in multiple fidelities',
    long_description=long_description,
    author='Sander van Rijn',
    author_email='s.j.van.rijn@liacs.leidenuniv.nl',
    packages=['multifidelityfunctions'],
)
