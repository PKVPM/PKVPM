#! /usr/bin/env python
# -*- coding: utf-8 -*-
# RUN Command Line:
# 1.Build-check dist folder
# python setup.py sdist bdist_wheel
# 2.Upload to PyPi
# twine upload dist/*

from setuptools import setup, find_packages

setup(
    name='pkvpm',
    version='1.0.0',
    author='PKVPM Organization',
    author_email='PKVPM@PKVPM.ORG',
    packages=find_packages(),
    install_requires=[
        'PyYAML'
    ],
    description='A package for Polymorphic Key-Value Path Mapping (PKVPM)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PKVPM/PKVPM',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
