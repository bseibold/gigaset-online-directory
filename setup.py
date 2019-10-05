#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name = 'gigaset',
    version = '0.1',
    author = 'Bernhard Seibold',
    author_email = 'mail@bernhard-seibold.de',
    description = ('A small web-app that serves as a proxy for phone number '
                   'lookups for Gigaset DECT base stations'),
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    license = 'MIT',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Communications :: Telephony',
    ],
    python_requires = '>=3.2',
)

