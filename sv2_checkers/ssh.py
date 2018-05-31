import re
import os
from os import popen, path
from sys import stderr

import psutil

from sv2.helpers import run_checkers


summary = "Check ssh configuration"

report = None


algorithm_blacklist = """
ecdh-sha2-nistp256 weak eliptic curves
ecdh-sha2-nistp384 weak eliptic curves
ecdh-sha2-nistp521 weak eliptic curves
diffie-hellman-group14-sha1 weak hash algorithm
ecdsa-sha2-nistp256 weak eliptic curves
hmac-sha1 weak hash algorithm
hmac-sha1-etm@openssh.com weak hash algorithm
"""


class _SSHConf(object):

    def __init__(self, conf):
        self.conf = [x.split(' ', 1) for x in conf.rsplit('\n')]
        self.confdict = dict()
        for x in self.conf:
            if len(x) > 1:
                if x[0] in self.confdict.keys():
                    self.confdict[x[0]] = (self.confdict[x[0]], x[1])
                else:
                    self.confdict.update({x[0]: x[1]})

    def __getitem__(self, x):
        return self.confdict[x]

    def getOptions(self):
        return self.confdict.keys()


class SSHCheck(object):

    def __init__(self):
        with popen("/usr/sbin/sshd -T 2>/dev/null") as p:
            sshd_config = p.read()
        self._sshd = _SSHConf(sshd_config)

    def root(self):
        if self._sshd["permitrootlogin"] != "no":
            report.new_issue("Disable root login.")

    def port(self):
        if self._sshd['port'] == '22':
            report.new_issue("Port number should not be the default (22).")

    def logingracetime(self):
        if int(self._sshd["logingracetime"]) > 25:
            report.new_issue(
                "LoginGraceTime is very high.")

    def passauthentication(self):
        if self._sshd["passwordauthentication"] == 'yes' or self._sshd["challengeresponseauthentication"] == 'yes':
            report.new_issue("Disable keyboard-interactive and use ssh keys instead (or combine it, for example ssh keys + OTP codes). Make sure than PasswordAuthentication and ChallengeResponseAuthentication is both disabled.")

    def TFA(self):
        with open("/etc/pam.d/sshd", 'r') as f:
            sshd_pam = f.read()
        if not re.match("\s*auth\s*required\s*pam_google_authenticator.so*", sshd_pam):
            report.new_issue("It is recommended use 2FA.")
            return 0
        opt_or_suff = re.match(
            "\s*auth\s*(optional|sufficient)\s*pam_google_authenticator.so*", sshd_pam)
        if opt_or_suff is not None:
            report.new_issue(
                "Not use {} option in /etc/pam.d/sshd.".format(opt_or_suff.group()))

    def login_filter(self):
        if not ("allowusers" in self._sshd.getOptions()) or ("allowgroups" in self._sshd.getOptions()):
            report.new_issue(
                "Filter users/groups with AllowUSers, and/or, AllowGroups.")

    def subsystem(self):
        if "subsystem" in self._sshd.getOptions():
            report.new_issue("If you do not really need {} disable it.".format(
                self._sshd["subsystem"]))

    def algorithm(self):
        for item in algorithm_blacklist.strip().splitlines():
            item_cleared = item.split(' ', 1)
            for x in self._sshd.conf:
                if len(x) > 1:
                    if item_cleared[0] in x[1]:
                        report.new_issue(
                            "{} - {}".format(item_cleared[0], item_cleared[1][:-1]))
                        break

    def fail2ban(self):
        if not path.exists("/usr/bin/fail2ban-server"):
            report.new_issue("Fail2ban not installed.")


def run(r, opts):
    global report
    report = r
    c = SSHCheck()
    run_checkers(c, opts)


def makes_sense(r) -> bool:
    if os.geteuid() != 0:
        r.wont_run("Needs root")
        return False

    for process in psutil.process_iter():
        if process.name() == "sshd":
            return True

    r.wont_run("SSH daemon is not running")
    return False

