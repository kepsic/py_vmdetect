# -*- coding: utf-8 -*-

"""Unit test package for py_vmdetect."""
import unittest
import tests.test_py_vmdetect


def my_module_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(tests.test_py_vmdetect)
    return suite
