import importlib
import argparse
import pkgutil
import sys


class Report:

    def __init__(self, name):
        self.name = name
        self.issues = []
        self.reason = None
    
    def new_issue(self, msg):
        self.issues.append(msg)

    def wont_run(self, reason):
        self.reason = reason


class ReportManager:

    def __init__(self, hide_inactive):
        self._reports = []
        self._hide_inactive = hide_inactive

    def add_report(self, r):
        self._reports.append(r)

    def print(self):
        for r in self._reports:
            if self._hide_inactive and r.reason:
                continue

            print("REPORTS FOR " + r.name)        
            if r.reason:
                print(r.name + " didn't run because " + r.reason) 
            else:
                for i in r.issues:
                    print(i)
            if r != self._reports[-1]:
                print("")

def setup_args():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    # TODO: Allow to exclude/include single checks of a given checkers, 
    #   like --exclude a.sub_a a.sub_b
    g.add_argument('--only', nargs='+', help='Only run the next checkers')
    g.add_argument('--exclude', nargs='+', help='Exclude the given checkers')
    g.add_argument('--list-checkers', action="store_true", help='List available checkers')
    parser.add_argument('--hide-inactive', action="store_true", help="Hide checkers that won't run")
    return parser

def get_available_checkers():
    m = importlib.import_module("sv2_checkers")
    return [s[1] for s in pkgutil.walk_packages(m.__path__)]

def import_checkers(l):
    return [importlib.import_module("sv2_checkers." + m) for m in l]

def list_checkers(l):
    print("LIST OF AVAILABLE CHECKERS")
    for m in l:
        summary = importlib.import_module("sv2_checkers." + m).summary
        print("{}: {}".format(m, summary))

def run_checkers(checkers, r_manager):
    for c in checkers:
        r = Report(c.__name__.split(".")[-1])
        if c.makes_sense(r):
            c.run(r)
        r_manager.add_report(r)
    return r_manager

if __name__ == "__main__":
    parser = setup_args()
    args = parser.parse_args()
    checkers = get_available_checkers()

    if args.exclude:
        for i in args.exclude:
            checkers.remove(i)

    if args.only:
        # TODO: Check that provided checkers are valid
        checkers = args.only

    if args.list_checkers:
        list_checkers(checkers)
    else:
        repots = ReportManager(args.hide_inactive)
        checkers_modules = import_checkers(checkers)
        run_checkers(checkers_modules, repots)     
        repots.print()   