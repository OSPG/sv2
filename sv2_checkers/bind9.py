import os
import stat
import psutil
import grp

from sv2.helpers import run_checkers


summary = "Check bind9"

report = None


class Bind9:

    def check_user(self):
        for process in psutil.process_iter():
            if process.name() == "named":
                if process.username() == "root":
                    report.new_issue("Run bind9 with non-root user.")

    def check_perms(self):
        binddir = os.stat("/etc/bind")
        if binddir.st_uid != 0:
            report.new_issue("Owner of /etc/bind should be root.")
        if grp.getgrgid(binddir.st_gid).gr_name != "bind":
            report.new_issue("Group of /etc/bind should be bind.")
        perms = os.stat("/etc/bind")
        if stat.filemode(perms.st_mode)[-1] != "-":
            report.new_issue("Users should have not access to /etc/bind")

    def check_allow(self):
        with open("/etc/bind/named.conf.options", 'r') as f:
            conf = f.read()
            if "allow-recursion" not in conf:
                report.new_issue(
                    "Use allow-recursion to restric recursive queries to trusted clients.")
            if "allow-query" not in conf:
                report.new_issue(
                    "Use allow-query to restric queries to trusted clients.")
            if "allow-transfer" not in conf:
                report.new_issue(
                    "Use allow-transfer to restirct zone transfer to trusted hosts.")


def run(r, opts):
    global report
    report = r
    c = Bind9()
    run_checkers(c, opts)


def makes_sense(r) -> bool:
    # We should extent the check to ensure that this is not another program
    # with the same name.
    for process in psutil.process_iter():
        if process.name() == "named":
            return True

    r.wont_run("Bind9 is not running")
    return False
