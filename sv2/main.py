import importlib
import argparse
import pkgutil
import sys

import colorama

from sv2.helpers import get_public_class, get_public_members


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
    # TODO: Maybe be should add the possibility to set a level of priority

    def __init__(self, hide_inactive, verbose):
        self._reports = []
        self._hide_inactive = hide_inactive
        self._verbose = verbose

    def add_report(self, r):
        self._reports.append(r)

    def print(self):
        colorama.init()
        for r in self._reports:
            if self._hide_inactive and r.reason:
                continue

            if not r.reason and len(r.issues) == 0:
                if self._verbose:
                    print(colorama.Fore.GREEN, end='')
                    print(r.name + ": NO issues found")
                continue

            print(colorama.Fore.WHITE, end="")
            print("Reports for {} checker".format(r.name))
            if r.reason:
                print(colorama.Fore.BLUE, end="")
                print("\t\"{}\" check did not run ({})".format(r.name, r.reason))
            else:
                print(colorama.Fore.YELLOW, end="")
                for i in r.issues:
                    print("\t"+i)
            if r != self._reports[-1]:
                print("")
            else:
                print(colorama.Style.RESET_ALL, end="")


def setup_args():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--list-checkers', action="store_true",
                   help='List available checkers')
    g.add_argument('--list-all-checkers', action="store_true",
                   help='List all available checkers')
    parser.add_argument('--select', nargs='+', help='Select checkers to be run')
    parser.add_argument('--exclude', nargs='+', help='Exclude the given checkers')
    parser.add_argument('--hide-inactive', action="store_true",
                        help="Hide checkers that won't run")
    parser.add_argument('--verbose', action='store_true',
                        help='Tell which checkers had no issues')
    return parser


def get_available_checkers():
    m = importlib.import_module("sv2_checkers")
    return [s[1] for s in pkgutil.walk_packages(m.__path__)]


def import_checker(name):
    return importlib.import_module("sv2_checkers." + name)

def import_checkers(l):
    return [import_checker(m) for m in l]

def retrieve_checker_methods(module):
    methods_list = []
    for c in get_public_class(module):
        for member in get_public_members(getattr(module, c)):
            methods_list.append(member)
    return methods_list

def list_checkers(l):
    print("LIST OF AVAILABLE CHECKERS")
    for module in import_checkers(l):
        name = module.__name__.split(".")[1]
        summary = module.summary
        print(colorama.Fore.WHITE, end='')
        print("\t{}: ".format(name), end='')
        print(colorama.Fore.BLUE, end='')
        print(summary)
        print(colorama.Style.RESET_ALL, end="")


def list_all_checkers(l):
    print("LIST OF ALL AVAILABLE CHECKERS")
    for module in import_checkers(l):
        summary = module.summary
        name = module.__name__.split(".")[1]
        print(colorama.Fore.WHITE, end="")
        print("\tList of {} checks".format(name))
        print(colorama.Fore.BLUE, end="")
        for member in retrieve_checker_methods(module):
            print("\t\t", member)
        print(colorama.Style.RESET_ALL, end="")


def run_checkers(checkers, r_manager, opts):
    for c in checkers:
        name = c.__name__.split(".")[-1]
        r = Report(name)
        if c.makes_sense(r):
            c.run(r, opts[name])
        r_manager.add_report(r)
    return r_manager


def initialize_checkers_options(checkers):
    checkers_options = {}
    for i in checkers:
        checkers_options[i] = {"exclude_list": [], "select_list": []}

    return checkers_options


def main():
    parser = setup_args()
    args = parser.parse_args()
    checkers = get_available_checkers()
    checkers_options = initialize_checkers_options(checkers)

    if args.exclude:
        for i in args.exclude:
            if "." in i:
                name, check = i.split(".")
                checkers_options[name]["exclude_list"].append(check)
            else:
                checkers.remove(i)

    if args.select:
        checkers = []
        # TODO: Check that provided checkers are valid
        for i in args.select:
            if "." in i:
                name, check = i.split(".")
                checkers_options[name]["select_list"].append(check)
                if name not in checkers:
                    checkers.append(name)
            else:
                checkers.append(i)

    if args.list_checkers:
        list_checkers(checkers)
    elif args.list_all_checkers:
        list_all_checkers(checkers)
    else:
        repots = ReportManager(args.hide_inactive, args.verbose)
        checkers_modules = import_checkers(checkers)
        run_checkers(checkers_modules, repots, checkers_options)
        repots.print()


if __name__ == "__main__":
    main()
