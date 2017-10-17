#!/usr/bin/env python
from setuptools import setup, find_packages


gins_dev = {'develop': [
    "pep8-naming>=0.3.3",   # MIT license
    "flake8>=2.5.1",        # MIT license
    "pyflakes>=1.0.0",      # MIT license
    "coverage",
    ]
}

extras_require = ['numpy', 'scipy', 'matplotlib']

setup(
    name='gins',
    version='0.0.1',
    description='Gins (Graph inspector) is a CLI tool for inspecting, creating graphs and much more. Works with NetworkX',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/gins',
    packages=find_packages(),
    test_suite='gins.tests',
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
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: PyPy"
    ],

    install_requires=[
        'click',              # MIT license
        'networkx'             # MIT license
    ] + extras_require,

    scripts=['bin/gins'],
    extras_require=gins_dev
)
