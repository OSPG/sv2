import psutil

from sv2.helpers import run_checkers


summary = "Check mount options"

report = None


class MountCheck:

    def __init__(self):
        self._partitions = psutil.disk_partitions(all=True)

    def tmp(self):
        for i in self._partitions:
            if i[1] == "/tmp":
                if not "noexec" in i[3] or "nosuid" not in i[3] \
                        or "nodev" not in i[3]:
                    report.new_issue("/tmp mountpoint should have noexec and nosuid options.")
                    return
        report.new_issue(
            "/tmp should be separated and have noexec, nosuid and nodev options.")

    def home(self):
        for i in self._partitions:
            if i[1] == "/home":
                return
        report.new_issue("/home should be separated.")

    def tmpfs(self):
        for i in self._partitions:
            if i[0] == "tmpfs" and i[0] != "/tmp":
                if "nosuid" not in i[3] or "nodev" not in i[3]:
                    report.new_issue(
                        "{} should have nosuid and nodev options.".format(i[1]))

    def usage(self):
        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition[1])[-1]
            if usage >= 90:
                report.new_issue("Usage of {}: {}%".format(partition[1], usage))

def run(r, opts):
    global report
    report = r
    c = MountCheck()
    run_checkers(c, opts)


def makes_sense(r):
    return True
