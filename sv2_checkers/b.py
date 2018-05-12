from sv2.helpers import get_public_members

summary = "TEST"

class Test:
    def __init__(self, report):
        self._report = report

    def a(self):
        self._report.new_issue("Test.a")

    def b(self):
        self._report.new_issue("Test.b")


def run(report, opts):
    c = Test(report)

    m_l = get_public_members(Test)
    if opts["exclude_list"]:
        for i in opts["exclude_list"]:
            m_l.remove(i)
    elif opts["only_list"]:
        m_l = opts["only_list"]

    for m in m_l:
        getattr(c, m)()

def makes_sense(report):
    return True