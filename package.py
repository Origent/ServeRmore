#!python3

import VERSION, boto3
from setuptools import setup

def package_build():
    from distutils.core import run_setup
    run_setup('setup.py', script_args=['sdist'])

def package_test():
    import subprocess
    import sys
    COMMAND="pip uninstall serveRmore -y"
    result = subprocess.call(COMMAND,shell=True)
    COMMAND="pip install dist/serveRmore-"+VERSION.VERSION+".tar.gz"
    result = subprocess.call(COMMAND,shell=True)
    COMMAND="srm settings"
    result = subprocess.call(COMMAND,shell=True)

package_build()
package_test()
