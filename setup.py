#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import sys
import os

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

sources = ['py_vmdetect/src/vmdetect.cpp']
libraries = []
include_dirs = [ ]    # may be changed by pkg-config
define_macros = []
library_dirs = []
extra_compile_args = ['-fPIC']
extra_link_args = ['-shared']

requirements = ['Click>=6.0',
                'cffi>=1.12.3'
                ]

setup_requirements = [ ]

test_requirements = [ ]

no_compiler_found = False
def no_working_compiler_found():
    sys.stderr.write("""
    No working compiler found, or bogus compiler options passed to
    the compiler from Python's standard "distutils" module.  See
    the error messages above.  Likely, the problem is not related
    to CFFI but generic to the setup.py of any Python package that
    tries to compile C code.  (Hints: on OS/X 10.8, for errors about
    -mno-fused-madd see http://stackoverflow.com/questions/22313407/
    Otherwise, see https://wiki.python.org/moin/CompLangPython or
    the IRC channel #python on irc.freenode.net.)

    Trying to continue anyway.  If you are trying to install CFFI from
    a build done in a different context, you can ignore this warning.
    \n""")
    global no_compiler_found
    no_compiler_found = True

def get_config():
    from distutils.core import Distribution
    from distutils.sysconfig import get_config_vars
    get_config_vars()      # workaround for a bug of distutils, e.g. on OS/X
    config = Distribution().get_command_obj('config')
    return config

def test_copiler():
    config = get_config()
    ok1 = config.try_compile('int some_regular_variable_42;')
    if not ok1:
        no_working_compiler_found()

def _safe_to_ignore():
    sys.stderr.write("***** The above error message can be safely ignored.\n\n")


if 'freebsd' in sys.platform:
    include_dirs.append('/usr/local/include')
    library_dirs.append('/usr/local/lib')

if __name__ == '__main__':
    from setuptools import setup, Distribution, Extension, find_packages
    test_copiler()


    class VMDetectDistribution(Distribution):
        def has_ext_modules(self):
            # Event if we don't have extension modules (e.g. on PyPy) we want to
            # claim that we do so that wheels get properly tagged as Python
            # specific.  (thanks dstufft!)
            return True

    setup(
        author="Andres Kepler",
        author_email='andres@kepler.ee',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        description="Python virtual machine detection tool detects virtual environment - VMWare, XEN, FreeBSD jail etc",
        entry_points={
            'console_scripts': [
                'py_vmdetect=py_vmdetect.cli:main',
            ],
        },
        install_requires=requirements,
        license="MIT license",
        long_description=readme + '\n\n' + history,
        include_package_data=True,
        keywords='py_vmdetect',
        name='py_vmdetect',
        packages=find_packages(include=['py_vmdetect']),
        setup_requires=setup_requirements,
        test_suite='tests',
        tests_require=test_requirements,
        url='https://github.com/kepsic/py_vmdetect',
        version='0.1.4',
        zip_safe=False,
        distclass=VMDetectDistribution,
        ext_modules=[Extension(
                name='_vmdetect_backend',
                include_dirs=include_dirs,
                sources=sources,
                libraries=libraries,
                define_macros=define_macros,
                library_dirs=library_dirs,
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args
            )]

    )
