from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='aprovafacil',
      version=version,
      description="Wrapper for the AprovaFacil CGI",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='cobrebem aprovafacil payment credit-card',
      author='Vitor M. A. da Cruz',
      author_email='vitor.mazzi@myfreecomm.com.br',
      url='http://www.myfreecomm.com.br',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        'httplib2',
        'IPy',
        'Mock',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
