# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='exectree',
    version='0.0.1',
    description='Build execution tree from recursive functions',
    long_description=readme,
    author='Felix Martel-Denis',
    url='https://github.com/FelixMartel/exectree',
    license=license,
    packages=find_packages(exclude=('tests'))
)

