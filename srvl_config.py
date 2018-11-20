#!/usr/bin/env python

import ctypes, os, io, yaml
from pathlib import Path

class srvlConfig:

    def __init__(self):
        self.file = str(Path.home())+"/serveRmore.yaml"
        self.settings = {}
        self.pwd = os.getcwd()
        os.chdir(str(Path.home())+"/")
        self.load_all()

    def check(self):
        str = "Please edit your ~/serveRmore.yaml file and add the following:\n"
        print_msg = 0
        if not self.settings["git"]["private_key"]:
            str = str + "Add Github private key\n"
            print_msg += 1
        if not self.settings["aws"]["private_key"]:
            str = str + "Add AWS private key\n"
            print_msg += 1
        if not self.settings["aws"]["subnet"]:
            str = str + "Add Subnet ID\n"
            print_msg += 1
        if not self.settings["aws"]["sec_group"]:
            str = str + "Add AWS Security Group w/ SSH port open\n"
            print_msg += 1
        if not self.settings["aws"]["s3_bucket"]:
            str = str + "Add AWS S3 Bucket Name\n"
            print_msg += 1
        if not self.settings["aws"]["s3_key"]:
            str = str + "Add AWS S3 Bucket Key\n"
            print_msg += 1
        if not self.settings["lambda"]["name"]:
            str = str + "Add AWS Lambda Function Name\n"
            print_msg += 1
        if not self.settings["lambda"]["handler_path"]:
            str = str + "Add AWS Lambda handler.py Path + Filename\n"
            print_msg += 1
        if not self.settings["builder"]["custom_r_package_file"]:
            str = str + "Add Filename of your custom R package\n"
            print_msg += 1
        if print_msg > 0:
            print(str)

    def show(self):
        if not self.exists():
            return False
        else:
            print(yaml.dump(self.load(), default_flow_style=False))

    def version(self):
        print("ServeRmore 0.0.1")

    def load_all(self):
        self.settings = self.load()

    def write_all(self):
        for key in self.settings:
            for name in self.settings[key]:
                self.write(key,name, self.settings[key][name])

    def set(self, key, name, value):
        self.settings[key][name] = value
        self.write(key,name,value)

    def read(self, key, name):
        self.settings = self.load()
        if not self.settings[key][name]:
            return False
        else:
            return self.settings[key][name]

    def write(self, key, name, value):
        self.settings = self.load()
        self.settings[key][name] = value
        with io.open(self.file, 'w', encoding='utf8') as outfile:
            yaml.dump(self.settings, outfile, default_flow_style=False, allow_unicode=True)

    def load(self):
        if not self.exists():
            self.settings = self.reset()
            with io.open(self.file, 'w', encoding='utf8') as outfile:
                yaml.dump(self.settings, outfile, default_flow_style=False, allow_unicode=True)
        with open(self.file, 'r') as stream:
            return yaml.load(stream)

    def replace(self):
        if self.exists():
            os.replace(self.file, self.file + ".old")

    def exists(self):
        if os.path.isfile(self.file):
            return True
        else:
            return False

    def help(self):
        s = """\nPlease use the following commands for AWS:
    srm help | settings | version
    srm create | update | package | deploy | test | terminate
    srm status | ssh | sftp\n"""
        print(s)

    def reset(self):
        return yaml.load("""
        git:
            repo: git@github.com:Origent/ServeRmore.git
            private_key: github.pem
        aws:
            s3_bucket:
            s3_key:
            private_key: aws.pem
            subnet:
            sec_group:
        builder:
            ami: ami-4fffc834
            instance_type: t2.medium
            instance_id:
            domain_name:
            public_ip:
            custom_r_package_file:
            cran_r_package_names: ['survival', 'gbm', 'jsonlite']
        lambda:
            name:
            handler_path:
        """)
