#!python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='serveRmore',
    version='0.0.1',
    author='Andrew Conklin',
    author_email='aconklin@origent.com',
    scripts=['README.md'],
    py_modules = ['ServeRlmore', 'srvl_config', 'srvl_connect'],
    install_requires=['paramiko', 'boto3', 'pyyaml'],
    python_requires='>=3',
    url='https://github.com/Origent/ServeRmore.git',
    license='GPL v3',
    classifiers=[
        "Programming Language :: Python :: 3.x",
        "Operating System :: OS Independent",
    ],)
