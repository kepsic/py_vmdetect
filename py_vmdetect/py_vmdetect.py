# -*- coding: utf-8 -*-
import os.path
from cffi import FFI


class VMDetect():
    vm_providers = {
        1: "VM_OPENVZ",
        2: "VM_XEN",
        3: "VM_VMWARE",
        4: "VM_KVM",
        5: "VM_HYPERV",
        6: "VM_USERMODELINUX",
        7: "VM_FREEBSDJAIL",
    }
    def __init__(self):
        ffi = FFI()
        ffi.cdef("int vm_by_cpuid();\
                  int isVMware();\
                  int isHyperV();\
                  int detectVZ();\
                  int isUserModeLinuxOrKvm();\
                  int detect_XEN_domU();\
                  int detectFreeBSDJAIL();\
                  ")
        path_string = os.path.dirname(os.path.realpath(__file__)) + "/vmdetect.so"
        self.vmdetect  = ffi.dlopen(path_string)

    def vm_provider_id(self):
        r = self.vmdetect.vm_by_cpuid()
        return r

    def is_vm(self):
        return self.isVMware() or \
               self.isHyperV() or \
               self.isOpenVZ() or \
               self.isUserModeLinux() or \
               self.isKvm() or \
               self.isXENDomU() or \
               self.isFreeBSDJAIL()

    def vm_provider_by_cpuid(self):
        r = self.vmdetect.vm_by_cpuid()
        return self.vm_providers.get(r, "UNKNOWN")

    def isOpenVZ(self):
        r = self.vmdetect.detectVZ()
        return r == 1

    def isXENDomU(self):
        r = self.vmdetect.detect_XEN_domU()
        return r == 2

    def isVMware(self):
        r = self.vmdetect.isVMware()
        return r == 3

    def isKvm(self):
        r = self.vmdetect.isUserModeLinuxOrKvm()
        return r == 4

    def isHyperV(self):
        r = self.vmdetect.isHyperV()
        return r == 5

    def isUserModeLinux(self):
        r = self.vmdetect.isUserModeLinuxOrKvm()
        return r == 6

    def isFreeBSDJAIL(self):
        r = self.vmdetect.detectFreeBSDJAIL()
        return r == 7
