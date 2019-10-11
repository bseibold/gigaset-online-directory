#!/usr/bin/env python3

"""A small web-app that serves as a proxy for phone number
lookups for Gigaset DECT base stations"""

from setuptools import setup

with open('README.rst', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='gigaset',
    version='0.1',
    author='Bernhard Seibold',
    author_email='mail@bernhard-seibold.de',
    description=(__doc__),
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    license='MIT',
    packages=[
        'gigaset',
        'gigaset.backends',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Communications :: Telephony',
    ],
    python_requires='>=3.2',
    install_reqs=[
        'Flask>=1.0.0',
        'beautifulsoup4>=4.8.0',
    ],
    zip_safe=False,
)
