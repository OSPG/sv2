import platform
import psutil

from sv2.helpers import run_checkers


summary = "Check hidepid"

report = None


class HidePID:

    def hide_pid(self):
        for mountpoint in psutil.disk_partitions(all=True):
            if mountpoint.mountpoint == "/proc":
                if "hidepid" not in mountpoint.opts \
                        or "hidepid=0" in mountpoint.opts:
                    report.new_issue("Set hidepid mount option on /proc.")


def run(r, opts):
    global report
    report = r
    c = HidePID()
    run_checkers(c, opts)


def makes_sense(r) -> bool:
    if not platform.system() == "Linux":
        r.wont_run("SO is not Linux")
        return False

    return True
