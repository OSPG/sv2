import os
import iptc

from sv2.helpers import get_checkers_to_run

# TODO: This check should check if some firewall is used, not only iptables

summary = "Check if iptables are used"

report = None

class IptablesCheck:
    def __init__(self):
        count = 0
        t = iptc.Table(iptc.Table.FILTER)
        for c in t.chains:
            count += len(c.rules)

        if count == 0:
            self._used = False
        else:
            self._used = True

    def used(self):
        if not self._used:        
            report.new_issue("Iptables are not used")

def run(r, opts):
    global report
    report = r
    c = IptablesCheck()
    for m in get_checkers_to_run(IptablesCheck, opts):
        getattr(c, m)()

def makes_sense(r) -> bool:
    if os.geteuid() != 0:
        r.wont_run("Needs root")
        return False

    try:
        os.stat("/sbin/iptables")
        return True
    except:
        r.wont_run("Iptables is not present")
        return False
