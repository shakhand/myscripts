import argparse
import os
import re
import subprocess
import pickle

def _collect_all_unit_test():
    unitTests = {}
    rootDir = 'H:\\Source\\NetNodes\\PCtrl'
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            m = re.match(r'^rt_(.*?)\.sln$', fname)
            if m:
                filePath = os.path.abspath(os.path.join(dirName, fname))
                unitTestName = m.group(1)
                unitTests[unitTestName] = filePath
    return unitTests

def _get_unit_test_store():
    unit_test_store = None
    # try to read unit test from cache
    if os.path.exists('unit_test.cache'):
        with open('unit_test.cache', 'rb') as f:
            unit_test_store = pickle.load(f)

    # try to collect all unit tests and write to a cache file
    if unit_test_store is None:
        unit_test_store = _collect_all_unit_test()

        with open('unit_test.cache', 'wb') as f:
            pickle.dump(unit_test_store, f, pickle.DEFAULT_PROTOCOL)

    return unit_test_store

def action_list_all_unit_tests():
    unit_tests = _get_unit_test_store()

    for unit_test, _ in unit_tests.items():
        print(unit_test)

def action_match_unit_tests(pattern):
    unit_tests = _get_unit_test_store()

    for unit_test, _ in unit_tests.items():
        if re.match(r'.*%s.*'%pattern, unit_test, re.IGNORECASE):
            print(unit_test)

def action_build_unit_test(name):
    unit_tests = _get_unit_test_store()

    for unit_test, path in unit_tests.items():
        if re.match(name, unit_test, re.IGNORECASE):
            print('start to build unit test %s'%(unit_test))
            subprocess.call(['C:\\Program Files (x86)\Microsoft Visual Studio 8\Common7\IDE\devenv.com', unit_tests[unit_test], '/build', 'Debug'], shell=True)

def action_open_unit_test(name):
    unit_tests = _get_unit_test_store()

    for unit_test, path in unit_tests.items():
        if re.match(name, unit_test, re.IGNORECASE):
            print('open project %s'%unit_tests[unit_test])
            subprocess.call(['C:\\Program Files (x86)\Microsoft Visual Studio 8\Common7\IDE\devenv.com', unit_tests[unit_test]])

def action_recollect_unit_test():
    os.remove('unit_test.cache')
    action_list_all_unit_tests()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pctrl unit test runner')
    parser.add_argument("--list", '-l', action='store_true', help="list all unit test")
    parser.add_argument("--match", '-m', default='all', help="list unit test match the pattern")
    parser.add_argument('-a', "--buildall", action='store_true', help="build all unit test")
    parser.add_argument('-b', "--build", help='build a unit test')
    parser.add_argument('-p', "--project", help='open a unit test project')
    parser.add_argument('-r', "--recollect", action='store_true', help='recollect the unit tests in the root path')
    args = parser.parse_args()

    if args.list:
        action_list_all_unit_tests()

    elif args.match:
        action_match_unit_tests(args.match)

    if args.build:
        action_build_unit_test(args.build)

    if args.project:
        action_open_unit_test(args.project)

    if args.recollect:
        action_recollect_unit_test()



