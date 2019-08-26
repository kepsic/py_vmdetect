// This file origin is https://github.com/litespeedtech/lsmcd/blob/master/src/util/sysinfo/vmdetect.cpp
#include <fcntl.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#include <sys/wait.h>
#include <unistd.h>

#define VM_OPENVZ   1
#define VM_XEN      2
#define VM_VMWARE   3
#define VM_KVM      4
#define VM_HYPERV   5
#define VM_USERMODELINUX   6
#define VM_FREEBSDJAIL   7


static int  readFile(char *pBuf, int bufLen, const char *pName,
                     const char *pBase)
{
    char achFilePath[512];
    int fd;
    fd = open(achFilePath, O_RDONLY, 0644);
    if (fd == -1)
        return -1;
    int ret = read(fd, pBuf, bufLen);
    close(fd);
    return ret;
}

int _detectFreeBSDJAIL()
{
    int ret = 0;
#ifdef __FreeBSD__
    struct stat st;
    size_t len;
    int jailed;
    len = 4;
    sysctlbyname("security.jail.jailed", &jailed, &len, NULL, 0);

    if (stat("/", &st) == 0)
    {
        if (st.st_ino > 2 || jailed == 1)
            return VM_FREEBSDJAIL;
    }
#endif
    return ret;
}

int _detectVZ()
{
    int ret = 0;
#if defined(linux) || defined(__linux) || defined(__linux__)
    struct stat st;
    if (stat("/proc/vz/", &st) == 0)
    {
        if ((stat("/proc/vz/vestat", &st) == 0) ||
            (stat("/proc/vz/veinfo", &st) == 0))
        {
            if (stat("/proc/vz/vzquota", &st) == -1)
                return VM_OPENVZ;
        }
        int s = system("dmidecode 2>&1 | grep \"/dev/mem\" | grep -e \"\\(denied\\|not permitted\\)\" > /dev/null");
        if (WEXITSTATUS(s) == 0)
            return VM_OPENVZ;
    }
#endif
    return ret;
}


#include <setjmp.h>
#include <signal.h>
//#if defined(macintosh) || defined(__APPLE__) || defined(__APPLE_CC__)
//static int _isXEN()
//(({
//    return 0;
//}
//#else
//#if defined(__i386__)||defined( __x86_64 )||defined( __x86_64__ )
static unsigned int getcpuid(unsigned int eax, char *sig)
{
    unsigned int *sig32 = (unsigned int *) sig;

    asm volatile(
        "xchgl %%ebx,%1; xor %%ebx,%%ebx; cpuid; xchgl %%ebx,%1"
        : "=a"(eax), "+r"(sig32[0]), "=c"(sig32[1]), "=d"(sig32[2])
        : "0"(eax));
    sig[12] = 0;

    return eax;
}

static int _get_vm_type_by_cpuid(const char *cpuid)
{
    if (strncmp("XenVMMXenVMM", cpuid, 12) == 0)
        return VM_XEN;
    else if (strncmp("VMwareVMware", cpuid, 12) == 0)
        return VM_VMWARE;
    else if (strncmp("KVMKVMKVM", cpuid, 9) == 0)
        return VM_KVM;
    else if (strncmp("Microsoft Hv", cpuid, 12) == 0)
        return VM_HYPERV;

    return 0;
}

int _vm_by_cpuid() {
    int ret;
    char sig[13];
    unsigned int base = 0x40000000, leaf = base;
    unsigned int max_entries;

    memset(sig, 0, sizeof sig);
    max_entries = getcpuid(leaf, sig);
    ret = _get_vm_type_by_cpuid(sig);
    if (ret)
        return ret;
    if (max_entries > 3 && max_entries < 0x10000)
    {
        for (leaf = base + 0x100; leaf <= base + max_entries; leaf += 0x100)
        {
            memset(sig, 0, sizeof sig);
            getcpuid(leaf, sig);
            ret = _get_vm_type_by_cpuid(sig);
            if (ret)
                return ret;
        }
    }
    return 0;
}


int _detect_XEN_domU()
{
    int ret = 0;
    struct stat st;
    if (stat("/proc/xen/capabilities", &st) == 0)
    {
        char achBuf[4096];
        readFile(achBuf, 4096, "/proc/xen/capabilities", "");
        if (strncmp(achBuf, "control_d", 9) != 0)
            ret = VM_XEN;
    }
    return ret;
}
//#endif //defined(__i386__)||defined( __x86_64 )||defined( __x86_64__ )
//#endif

static jmp_buf no_vmware;

static void handler(int sig)
{
    longjmp(no_vmware, 1);
}

#define VMWARE_MAGIC        0x564D5868  // Backdoor magic number
#define VMWARE_PORT         0x5658      // Backdoor port number
#define VMCMD_GET_VERSION   0x0a        // Get version number


#if defined(__i386__)||defined( __x86_64 )||defined( __x86_64__ )
int _isVMware()
{

    uint32_t eax = 0, ebx = 0, ecx = 0, edx = 0;
    int ret = 0;
#ifdef __FreeBSD__
#   define ERROR_SIGNAL SIGBUS
#else
#   define ERROR_SIGNAL SIGSEGV
#endif
    signal(ERROR_SIGNAL, handler);
    if (setjmp(no_vmware) == 0)
    {
        asm volatile("inl %%dx" :
                         "=a"(eax), "=c"(ecx), "=d"(edx), "=S"(ebx) :
                         "0"(VMWARE_MAGIC), "1"(VMCMD_GET_VERSION),
                         "2"(VMWARE_PORT) : "memory");
        ret = VM_VMWARE;
    }
    signal(ERROR_SIGNAL, SIG_DFL);

    return ret;
}
#endif


int _isUserModeLinuxOrKvm()
{
    int ret = 0;
#if defined(linux) || defined(__linux) || defined(__linux__)
    char achBuf[4096];
    int len = readFile(achBuf, 4095, "/proc/cpuinfo", "");
    achBuf[len] = 0;
    if (strstr(achBuf, "User Mode Linux"))
        ret = VM_USERMODELINUX;
    else if (strstr(achBuf, "QEMU Virtual CPU"))
        ret = VM_KVM;
#endif
    return ret;
}

int _isHyperV()
{
#if defined(linux) || defined(__linux) || defined(__linux__)
    char achBuf[4096];
    int len = readFile(achBuf, 4096, "/proc/ide/hdc/model", "");
    if ((len > 0) && (strncmp(achBuf, "Virtual ", 8) == 0))
    {
        len = readFile(achBuf, 4096, "/proc/acpi/fadt", "");
        if (len > 0)
        {
            char *pEnd = &achBuf[len];
            char *p = achBuf;
            while (p < pEnd)
            {
                p = (char *)memchr(p, 'V', pEnd - p);
                if (p)
                {
                    if (strncmp(p + 1, "RTUAL", 5) == 0)
                        return VM_HYPERV;
                    ++p;
                }
                else
                    break;
            }
        }
    }
#endif
    return 0;
}

extern "C" {

    extern int vm_by_cpuid() {
        return _vm_by_cpuid();
        }

    extern int isVMware() {
        return _isVMware();
        }

    extern int isHyperV() {
        return _isHyperV();
        }

    extern int detectVZ() {
        return _detectVZ();
        }

    extern int isUserModeLinuxOrKvm() {
        return _isUserModeLinuxOrKvm();
        }

    extern int detect_XEN_domU() {
        return _detect_XEN_domU();
        }

    extern int detectFreeBSDJAIL() {
        return _detectFreeBSDJAIL();
        }
}
