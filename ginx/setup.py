#!/usr/bin/env python
import os
from subprocess import call
from distutils.command.build_py import build_py as _build_py
from setuptools import setup, find_packages

ginx_dev = {'develop': [
    "pylint",      # MIT license
    "coverage",
    ]
           }

def get_version():
    """get_version"""
    with open('../VERSION.txt') as version:
        return version.read()

class install_numpy_scipy(_build_py):
    """Customized setuptools install command - because of strange bug with scipy"""
    call(['pip', 'install', 'numpy'])
    call(['pip', 'install', 'scipy'])
    call(['pip', 'install', 'pandas'])

setup(
    name='ginxcli',
    version=get_version(),
    description='Gins (Graph inspector) is a CLI tool for inspecting, creating graphs and much more. Works with NetworkX',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/ginx',
    packages=find_packages(),
    test_suite='ginx.tests',
    cmdclass={
        'install_numpy_scipy': install_numpy_scipy
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD3 License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'click',
        'networkx',
        'matplotlib'
    ],

    scripts=['bin/ginx'],
    extras_require=ginx_dev
)
