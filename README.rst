=========================================
Python virtual machine detection library
=========================================


.. image:: https://img.shields.io/pypi/v/py_vmdetect.svg
        :target: https://pypi.python.org/pypi/py_vmdetect

.. image:: https://img.shields.io/travis/kepsic/py_vmdetect.svg
        :target: https://travis-ci.org/kepsic/py_vmdetect

.. image:: https://readthedocs.org/projects/py-vmdetect/badge/?version=latest
        :target: https://py-vmdetect.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python virtual machine detection tool detects virtual enviroment - VMWare, XEN, FreeBSD jail eg


* Free software: MIT license
* Documentation: https://py-vmdetect.readthedocs.io.


Features
--------

* This pyhton library detects system eniroment. VMware, Xen, FreeBSD jail etc


```python
from py_vmdetect import VMDetect
vmd = VMDetect()
vmd.is_vm()
```


* Also installs py_vmdetect cli tool::

    $ py_vmdetect --test-type is_vm
    Is Virtual: no



Credits
-------

* This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
* The main core took from LSMCD_
* The C code is wrapped with cffi_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _LSMCD : https://github.com/litespeedtech/lsmcd/blob/master/src/util/sysinfo/vmdetect.cpp
.. _cffi : https://cffi.readthedocs.io
