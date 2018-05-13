import spwd
import stat
import pwd
import os

from sv2.helpers import run_checkers


summary = "Check users configuration"

report = None


# TODO: Check non-root users
class UsersCheck:
    def check_uid(self):
        for u in pwd.getpwall():
            if u.pw_uid == 0 and u.pw_name != "root":
                report.new_issue(
                    "There is a user with uid = 0 which is not root")

    def check_expiration(self):
        d = spwd.getspnam("root")
        if d.sp_expire == -1:
            report.new_issue("Enable expiration of users")

    def umask(self):
        with os.popen("umask") as p:
            val = p.read()
        if val[1:] != "77":
            report.new_issue("umask should be more restrictive (ie: 077)")

    def check_home(self):
        root_home = os.stat("/root")
        users_homes = os.scandir("/home")
        if root_home.st_mode & 0b111111:
            report.new_issue("Wrong permissions of /root")
        for user_home in users_homes:
            if user_home.is_dir() and os.stat(user_home.path).st_mode & 0b111111:
                report.new_issue(
                    "Wrong permissions of {}".format(user_home.path))


def run(r, opts):
    global report
    report = r
    c = UsersCheck()
    run_checkers(c, opts)


def makes_sense(r) -> bool:
    if os.geteuid() != 0:
        r.wont_run("Needs root to read /etc/shadow")
        return False
    return True
