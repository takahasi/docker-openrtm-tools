#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name="rtmdocker",
    version="1.0.1",
    url='https://github.com/takahasi/docker-openrtm-tools',
    author='takahasi',
    author_email='3263ta@gmail.com',
    maintainer='takahasi',
    maintainer_email='3263ta@gmail.com',
    description='Utility tool for docker container of OpenRTM-aist(OpenRTM on Docker)',
    long_description=readme,
    py_modules=["rtmdocker"],
    license="MIT",
    entry_points={
        'console_scripts': [
            'rtmdocker = rtmdocker.rtmdocker:main',
        ]
    }
)
