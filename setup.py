#!/usr/bin/env python


import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'soundcloud_cli',
    'author': 'Giulio Calacoci',
    'author_email': 'giulio.calacoci@2ndquadrant.it',
    'version': '0.1a1',
    'install_requires': ['soundcloud'],
    'packages': ['soundcloud_fdw'],
}

setup(**config)
