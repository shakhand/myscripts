import os
import re
import subprocess
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pctrl unit test runner')
    parser.add_argument('-l', dest=list, description="list all unit test")
    parser.add_argument('-a', dest=buildall, description="build all unit test")
    parser.add_argument('-b', dest=build, description='build a unit test')

    unitTests = {}
    # Set the directory you want to start from
    rootDir = 'H:\\Source\\NetNodes\\PCtrl'
    for dirName, subdirList, fileList in os.walk(rootDir):
        for fname in fileList:
            if re.match(r'^rt_.*?\.sln$', fname):
                filePath = os.path.abspath(os.path.join(dirName, fname))
                m = re.match(r'.*rt_(.*?)\.sln', fname)
                unitTestName = m.group(1)
                unitTests[unitTestName] = filePath

# list all unit test projects found
    for (ut, path) in unitTests.items():
        print(ut)

    subprocess.call(['C:\\Program Files (x86)\Microsoft Visual Studio 8\Common7\IDE\devenv.com', unitTests['CM'], '/build', 'Debug']
        , shell=True)