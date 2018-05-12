import os

from sv2.helpers import get_checkers_to_run


summary = "Check if usbguard is installed"

report = None

class USBGuard:

    def check_usb_guard(self):
        try:
            os.stat("/usr/bin/usbguard")
        except FileNotFoundError:
            report.new_issue("usbguard is not installed.")

def run(r, opts):
    global report
    report = r
    c = USBGuard()
    for m in get_checkers_to_run(USBGuard, opts):
        getattr(c, m)()

def makes_sense(r) -> bool:
    try:
        os.stat("/sys/bus/usb")
        return True
    except:
        r.wont_run("System don't seems to have support for usb")
        return False
