#!/usr/bin/python3

from setuptools import setup

setup(name='juliet',
      version='0.1-alpha.1',
      description='The lightweight static website generator',
      url='http://github.com/hlef/juliet',
      author='Hugo Lefeuvre',
      author_email='hle@owl.eu.com',
      license='MIT',
      packages=['juliet'],
      scripts=['juliet.py'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
