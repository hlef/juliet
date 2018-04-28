#!/usr/bin/python3

from setuptools import setup
import juliet

setup(name='juliet',
      version=juliet.__version__,
      description='The lightweight static website generator',
      url='http://github.com/hlef/juliet',
      author=juliet.__author__,
      author_email=juliet.__author_email__,
      license='MIT',
      packages=['juliet'],
      entry_points={
          'console_scripts': [
              'juliet = juliet:main'
          ]
      },
      zip_safe=False,
      install_requires = ['jinja2>=2.7', 'pygments', 'pyyaml>=3.11', 'markdown',
      'python-slugify'],
      test_suite='nose.collector',
      tests_require=['nose'])
