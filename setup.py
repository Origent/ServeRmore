#!python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='serveRmore',
    version='0.0.2',
    description='Serve R more on Serverless.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Origent Data Sciences',
    author_email='cloudhosting@origent.com',
    scripts=['bin/srm', 'README.md'],
    py_modules = ['ServeRmore', 'srvl_config', 'srvl_connect'],
    install_requires=['paramiko', 'boto3', 'PyYAML', 'requests'],
    python_requires='>=3',
    url='https://github.com/Origent/ServeRmore.git',
    license='Apache License 2.0',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
)
