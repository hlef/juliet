#!/usr/bin/python3

from setuptools import setup
from distutils.util import convert_path
import os

name = 'juliet'
packages = ['juliet']
requires = ['jinja2>=2.7', 'pyyaml>=3.11', 'markdown', 'python-slugify', 'python-dateutil']

main_ns = {}
with open(convert_path(os.path.join(packages[0], 'version.py'))) as ver_file:
    exec(ver_file.read(), main_ns)

setup(name=name,
      version=main_ns['__version__'],
      description=main_ns['__description__'],
      url=main_ns['__url__'],
      author=main_ns['__author__'],
      author_email=main_ns['__author_email__'],
      license=main_ns['__license__'],
      packages=packages,
      package_data = {'juliet': ['resources/*.zip']},
      entry_points={'console_scripts': ['juliet = juliet:main']},
      zip_safe=False,
      install_requires = requires,
      extra_requires = {"codehilite": 'pygments'}
      test_suite='nose.collector',
      tests_require=['nose'])
