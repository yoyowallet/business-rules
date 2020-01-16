#! /usr/bin/env python

from __future__ import absolute_import
import setuptools
from setuptools import find_packages

from business_rules import __version__ as version

with open('HISTORY.rst') as f:
    history = f.read()

description = 'Python DSL for setting up business intelligence rules that can be configured without code'

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name='business-rules',
    version=version,
    description='{0}\n\n{1}'.format(description, history),
    author='amitkpandey-in',
    author_email='gh@amitkpandey.in',
    url='https://github.com/amitkpandey-in/business-rules',
    packages=find_packages(exclude=['tests']),
    license='MIT',
    install_requires=install_requires,
    classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ]
)
