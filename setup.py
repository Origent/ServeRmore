#!python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='serveRmore',
    version='0.0.1',
    description='Serve R more on Serve R less.',
    author='Origent Data Sciences',
    author_email='cloudhosting@origent.com',
    scripts=['bin/srm', 'README.md'],
    py_modules = ['ServeRmore', 'srvl_config', 'srvl_connect'],
    install_requires=['paramiko', 'boto3', 'PyYAML', 'requests'],
    python_requires='>=3',
    url='https://github.com/Origent/ServeRmore.git',
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3.x",
        "Operating System :: OS Independent",
    ],
)
