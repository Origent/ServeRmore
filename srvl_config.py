#!/usr/bin/env python

import ctypes, os, io, yaml
from pathlib import Path

class srvlConfig:

    def __init__(self):
        self.file = str(Path.home())+"/serve-R-less.yaml"
        self.settings = {}
        self.pwd = os.getcwd()
        os.chdir(str(Path.home())+"/")
        self.load_all()
        self.set("aws", "base_dir", os.getcwd())

    def check(self):
        if not self.settings["git"]["private_key"]:
            print('Please go to your ~/serve-R-less.yaml file and update your Github private key.')
        if not self.settings["aws"]["private_key"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS private key.')
        if not self.settings["aws"]["subnet"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS Subnet ID.')
        if not self.settings["aws"]["sec_group"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS Security Group with SSH port open.')
        if not self.settings["aws"]["s3_bucket"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS S3 Bucket and Key info.')
        if not self.settings["aws"]["s3_key"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS S3 Bucket and Key info.')
        if not self.settings["lambda"]["name"]:
            print('Please go to your ~/serve-R-less.yaml file and update your AWS Lambda info.')

    def show(self):
        if not self.exists():
            return False
        else:
            print(yaml.dump(self.load(), default_flow_style=False))

    def version(self):
        print("Serve-R-less 0.0.1")

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

    def reset(self):
        return yaml.load("""
        git:
            repo: git@github.com:Origent/serve-R-less.git
            private_key: github.pem
        aws:
            s3_bucket:
            s3_key:
            private_key: aws.pem
            base_dir:
            subnet:
            sec_group:
        builder:
            ami: ami-4fffc834
            instance_type: t2.medium
            instance_id:
            domain_name:
            public_ip:
            r_packages: ['survival', 'gbm', 'jsonlite']
        lambda:
            name:
            handler:
        """)
