#!/usr/bin/env python

from distutils.core import setup

setup(name='glamod-parser',
      version='0.1',
      description='GLAMOD CDM data parser',
      author='William Tucker',
      author_email='gward@python.net',
      url='https://github.com/glamod/glamod-parser/',
      packages=['db', 'parse'],
      install_requires =  ['openpyxl', 'psycopg2', 'python-dateutil', 'SQLAlchemy'],
     )