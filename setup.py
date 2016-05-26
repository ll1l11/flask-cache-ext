#!/usr/bin/env python

from codecs import open
from setuptools import setup


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='Flask-Cache-Ext',
    version='0.0.1',
    url='http://github.com/wasw100/flask-cache-ext',
    license='MIT',
    author='wasw100',
    author_email='wasw100@gmail.com',
    description="Extension of Flask-Cache.",
    long_description=readme,
    packages=['flask_cache_ext'],
    install_requires=['Flask-Cache'],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
