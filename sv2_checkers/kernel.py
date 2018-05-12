#!/usr/bin/env python3

import os.path
import platform
import gzip

from sv2.helpers import get_checkers_to_run


report = None

class KernelCheck:

    def __init__(self, config):
        if not config:
            raise Exception("Kernel configuration not found.")

        if config.endswith(".gz"):
            with gzip.open(config) as f:
                self._config_file = f.readlines()
        else:
            with open(config) as f:
                self._config_file = f.readlines()

    def _isYes(self, opt):
        for l in self._config_file:
            if l.strip() == "CONFIG_{}=y".format(opt):
                return True

        return False
    
    def heap_randomization(self):
        if self._isYes("COMPAT_BRK"):
            report.new_issue("Heap randomization is disabled. Enable it")

    def stack_protector(self):
        if self._isYes("CC_STACKPROTECTOR_NONE"):
            report.new_issue("Stack protector is completely disabled. Enable it")

    def legacy_vsyscall(self):
        if not self._isYes("LEGACY_VSYSCALL_NONE"):
            report.new_issue("Disable legacy vsyscall table")

    def modify_tld(self):
        if self._isYes("MODIFY_LDT_SYSCALL"):
            report.new_issue("Disable TLD modify feature")

    def dmesg_restricted(self):
        if not self._isYes("SECURITY_DMESG_RESTRICT"):
            report.new_issue("Restrict access to dmesg logs to avoid information leaks")

    def hardened_usercopy(self):
        if not self._isYes("HARDENED_USERCOPY"):
            report.new_issue("Enable hardened memory copies to/from the kernel")

    def static_usermodehelper(self):
        if not self._isYes("STATIC_USERMODEHELPER"):
            report.new_issue("Enable static usermode helper.")

    def refcount(self):
        if not self._isYes("REFCOUNT_FULL"):
            report.new_issue("Enable full refcounting")

    def fortify(self):
        if not self._isYes("FORTIFY_SOURCE"):
            report.new_issue("Enable fortify source")

    def randstruct_plugin(self):
        if not self._isYes("GCC_PLUGIN_RANDSTRUCT"):
            report.new_issue("Enable randstruct GCC plugin")

    def hardened_SLAB_freelist(self):
        if not self._isYes("SLAB_FREELIST_HARDENED"):
            report.new_issue("Enable SLUB freelist hardening")


def get_config_file() -> str:
    # On some distros the config file can also be found on /usr/src/linux but as long as
    # we can not ensure it is the current config file is better to avoid
    # it.

    # In case that no config file is found we can try to dynamically test if some protections
    # are really enabled

    r = platform.release()
    m = platform.machine()
    f_list = ["/proc/config", "/proc/config.gz", "/boot/config-{}".format(r),
              "/etc/kernels/kernel-config-{}-{}".format(m, r)]

    for f in f_list:
        if os.path.isfile(f):
            return f

def run(r, opts):
    global report
    report = r
    c = KernelCheck(get_config_file())

    for m in get_checkers_to_run(KernelCheck, opts):
        getattr(c, m)()

def makes_sense(r) -> bool:
    if not platform.system() == "Linux":
        r.wont_run("OS is not linux")
        return False
    elif get_config_file() == None:
        r.wont_run("Config file couldn't be found")
        return False

    return True


