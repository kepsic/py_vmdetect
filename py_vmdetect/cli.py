# -*- coding: utf-8 -*-

"""Console script for py_vmdetect."""
import re
import sys
import click
from py_vmdetect import VMDetect


@click.command()
@click.option('--test-type', type=click.Choice(['is_vm',
                                                'vm_provider_by_cpuid',
                                                'isVMware',
                                                'isHyperV',
                                                'isOpenVZ',
                                                'isUserModeLinux',
                                                'isKvm',
                                                'isXENDomU',
                                                'isFreeBSDJAIL'
                                                ]))
def main(test_type=None):
    """Console script for py_vmdetect."""
    vmd = VMDetect()

    if not test_type:
        click.echo("Is Virtual: {}".format("yes" if vmd.is_vm() else "no"))
        return 0

    if re.match('is_vm', test_type):
        click.echo("Is Virtual: {}".format("yes" if vmd.is_vm() else "no"))
    elif re.match('vm_provider_by_cpuid', test_type):
        click.echo("VM Provider by CPUID: {}".format(vmd.vm_provider_by_cpuid()))
    elif re.match('isVMware', test_type):
        click.echo("Is VMware: {}".format("yes" if vmd.isVMware() else "no"))
    elif re.match('isHyperV', test_type):
        click.echo("Is HyperV: {}".format("yes" if vmd.isHyperV() else "no"))
    elif re.match('isOpenVZ', test_type):
        click.echo("Is OpenVZ: {}".format("yes" if vmd.isOpenVZ() else "no"))
    elif re.match('isUserModeLinux', test_type):
        click.echo("Is UserModeLinux: {}".format("yes" if vmd.isUserModeLinux() else "no"))
    elif re.match('isKvm', test_type):
        click.echo("Is Kvm: {}".format("yes" if vmd.isKvm() else "no"))
    elif re.match('isXENDomU', test_type):
        click.echo("Is XEN: {}".format("yes" if vmd.isXENDomU() else "no"))
    elif re.match('isFreeBSDJAIL', test_type):
        click.echo("Is FreeBSD JAIL: {}".format("yes" if vmd.isFreeBSDJAIL() else "no"))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
