from setuptools import setup, find_packages

setup(name='lightning',
      version='0.1.0',
      description='Tools for reading ungridded lightning data',
      url='http://github.com/jsignell/lightning-tools',
      author='Julia Signell',
      author_email='jsignell@gmail.com',
      license='MIT',
      packages=['lightning'],
      zip_safe=False,
      # If any package contains *.r files, include them:
      package_data={'': ['*.r', '*.R']},
      include_package_data=True)