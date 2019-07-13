    
# from distutils.core import setup
from setuptools import setup


setup(name='CWrap',
      version='0.0',
      description='Automatical generate Cython wrappers from C header files',
      packages=['cwrap', 'cwrap.backend', 'cwrap.frontends', 
                'cwrap.frontends.gccxml',
                'cwrap.frontends.clang','cwrap.frontends.clang.clang',
                ],
      scripts=["bin/cwrap"],
      setup_requires=["Cython", "pytest-runner"],
      tests_require=["pytest"],
      # zip_safe needs to be false for pxd files to be available to cython cimport
      #   https://cython.readthedocs.io/en/latest/src/userguide/sharing_declarations.html
      zip_safe = False,
      )
