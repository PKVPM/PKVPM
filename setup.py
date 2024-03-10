# setup.py
from setuptools import setup, find_packages

setup(
    name='pkvpm',
    version='0.1.0',
    author='PKVPM Organization',
    author_email='PKVPM@PKVPM.ORG',
    packages=find_packages(),
    install_requires=[
        # List of project dependencies
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
