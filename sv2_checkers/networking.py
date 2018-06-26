import os
import platform

from sv2.helpers import run_checkers


summary = "Check common tcp/ip config"

report = None


class _Sysctl:
    def read(self, key):
        with open("/proc/sys/%s" % key.replace(".", "/")) as f:
            value = f.readline().strip()
        return value


class TCPIP:

    def __init__(self):
        self.sysctl = _Sysctl()

    def sync_cookies(self):
        if not int(self.sysctl.read("net.ipv4.tcp_syncookies")):
            report.new_issue("Enable net.ipv4.tcp_syncookies.")

    def rfc1337(self):
        if not int(self.sysctl.read("net.ipv4.tcp_rfc1337")):
            report.new_issue("Enable net.ipv4.tcp_rfc1337.")

    def rp_filter(self):
        if not int(self.sysctl.read("net.ipv4.conf.default.rp_filter")) \
                or not int(self.sysctl.read("net.ipv4.conf.all.rp_filter")):
            report.new_issue(
                "Enable net.ipv4.conf.default.rp_filter and net.ipv4.conf.all.rp_filter.")

    def tcp_timestamps(self):
        if int(self.sysctl.read("net.ipv4.tcp_timestamps")):
            report.new_issue("Disable net.ipv4.tcp_timestamps.")

    def log_martian_packets(self):
        if not int(self.sysctl.read("net.ipv4.conf.default.log_martians")) \
                or not int(self.sysctl.read("net.ipv4.conf.all.log_martians")):
            report.new_issue(
                "Enable net.ipv4.conf.default.log_martians and net.ipv4.conf.all.log_martians.")

    def icmp_ignore_broadcast(self):
        if not int(self.sysctl.read("net.ipv4.icmp_echo_ignore_broadcasts")):
            report.new_issue("Enable net.ipv4.icmp_echo_ignore_broadcasts.")

    def ignore_bogus(self):
        if not int(self.sysctl.read("net.ipv4.icmp_ignore_bogus_error_responses")):
            report.new_issue(
                "Enable net.ipv4.icmp_ignore_bogus_error_responses.")

    def bpf_jit_harden(self):
        if not int(self.sysctl.read("net.core.bpf_jit_enable")):
            return

        if os.geteuid() != 0:
            report.wont_run("needs root")
            return

        if not int(self.sysctl.read("net.core.bpf_jit_harden")):
            report.new_issue("Enable net.core.bpf_hit_harden.")


def run(r, opts):
    global report
    report = r
    c = TCPIP()
    run_checkers(c, opts)


def makes_sense(r) -> bool:
    if not platform.system() == "Linux":
        r.wont_run("OS is not linux")
        return False
    return True
