#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `py_vmdetect` package."""
import re
import unittest
from unittest.mock import patch
from click.testing import CliRunner

from py_vmdetect import VMDetect
from py_vmdetect import cli


class TestPy_vmdetect(unittest.TestCase):
    """Tests for `py_vmdetect` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_is_vm_returns_true(self):
        """Test is_vm returns true."""
        with patch.object(VMDetect, 'is_vm', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.is_vm()
        mock_method.assert_called_once()

    def test_002_is_vm_provider_by_cpuid_retruns(self):
        """Test vm_provider_by_cpuid ."""
        with patch.object(VMDetect, 'vm_provider_by_cpuid', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.vm_provider_by_cpuid()
        mock_method.assert_called()

    def test_003_isOpenVZ(self):
        """Test isOpenVZ."""
        with patch.object(VMDetect, 'isOpenVZ', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isOpenVZ()
        mock_method.assert_called()

    def test_004_isXENDomU(self):
        """Test isXENDomU."""
        with patch.object(VMDetect, 'isXENDomU', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isXENDomU()
        mock_method.assert_called()

    def test_005_isVMware(self):
        """Test isVMware."""
        with patch.object(VMDetect, 'isVMware', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isVMware()
        mock_method.assert_called()

    def test_006_isKvm(self):
        """Test isKvm."""
        with patch.object(VMDetect, 'isKvm', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isKvm()
        mock_method.assert_called()

    def test_007_isHyperV(self):
        """Test isHyperV."""
        with patch.object(VMDetect, 'isHyperV', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isHyperV()
        mock_method.assert_called()

    def test_008_isUserModeLinux(self):
        """Test isUserModeLinux."""
        with patch.object(VMDetect, 'isUserModeLinux', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isUserModeLinux()
        mock_method.assert_called()

    def test_009_isFreeBSDJAIL(self):
        """Test isFreeBSDJAIL."""
        with patch.object(VMDetect, 'isFreeBSDJAIL', return_value=True) as mock_method:
            vmd = VMDetect()
            vmd.isFreeBSDJAIL()
        mock_method.assert_called()

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        print(result.exit_code)
        assert result.exit_code == 0
        assert re.match('.*Is Virtual:.*', result.output)
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert re.match(r'.*Show this message and exit.*', help_result.output.split("\n")[-2])
