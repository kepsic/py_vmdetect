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
include_dirs = []  # may be changed by pkg-config
define_macros = []
library_dirs = []
extra_compile_args = ['-fPIC',]
extra_link_args = ['-shared']

requirements = ['Click>=6.0',
                'cffi>=1.12.3'
                ]

setup_requirements = []

test_requirements = []

no_compiler_found = False

if 'freebsd' in sys.platform:
    include_dirs.append('/usr/local/include')
    library_dirs.append('/usr/local/lib')

if __name__ == '__main__':
    from setuptools import setup, Distribution, Extension, find_packages

    #test_copiler()
    #cpython = ('_vmdetect_backend' not in sys.builtin_module_names)


    class VMDetectDistribution(Distribution):
        def has_ext_modules(self):
            # Event if we don't have extension modules (e.g. on PyPy) we want to
            # claim that we do so that wheels get properly tagged as Python
            # specific.  (thanks dstufft!)
            return True


    class VMDetectExtension(Extension):
        def __init__(self, name, sources, *args, **kw):
            if 'darwin' in sys.platform:
                os.environ["CC"] = 'clang'
                os.environ["CXX"] = 'clang++'
                os.environ["CFLAGS"] = "-stdlib=libc++ -mmacosx-version-min=10.12 -fno-strict-aliasing -Wsign-compare -fno-common -dynamic " \
                                       "-DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -arch x86_64 -g -fPIC"
                os.environ["LDSHARED"] = "clang++ -stdlib=libc++ -undefined dynamic_lookup " \
                                         "-mmacosx-version-min=10.12 " \
                                         "-arch x86_64 -g -shared"
            Extension.__init__(self, name, sources, *args, **kw)


    setup(
        author="Andres Kepler",
        author_email='andres@kepler.ee',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        python_requires='>=3.6',
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
        version='0.2.2',
        zip_safe=False,
        distclass=VMDetectDistribution,
        ext_modules=[VMDetectExtension(
            name='_vmdetect_backend',
            include_dirs=include_dirs,
            sources=sources,
            libraries=libraries,
            define_macros=define_macros,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            language = 'c'
        )],


    )
