import os

from sv2.helpers import run_checkers


summary = "Check if coredumps are enabled"


class CoreDump:

    def __init__(self, report):
        self._report = report

    def core_dump_enabled(self):
        if os.popen("ulimit -c").read() != "0\n":
            self._report.new_issue(
                "It's recomended to disable core dumps to avoid information leakeage")


def run(report, opts):
    c = CoreDump(report)
    run_checkers(c, opts)


def makes_sense(report):
    return True
