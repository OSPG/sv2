import os
from sv2.helpers import get_public_members

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

    m_l = get_public_members(CoreDump)
    if opts["exclude_list"]:
        for i in opts["exclude_list"]:
            m_l.remove(i)
    elif opts["only_list"]:
        m_l = opts["only_list"]

    for m in m_l:
        getattr(c, m)()


def makes_sense(report):
    return True