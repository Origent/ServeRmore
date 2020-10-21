#!/usr/bin/env python

import ctypes, os, io, yaml
from pathlib import Path

class srvlConfig:

    def __init__(self):
        self.file = str(Path.home())+"/serveRmore.yaml"
        self.settings = {}
        self.pwd = os.getcwd()
        self.print_msg = 0
        os.chdir(str(Path.home())+"/")
        self.load_all()

    def show(self):
        if not self.exists():
            return False
        else:
            print(yaml.dump(self.load(), default_flow_style=False))

    def version(self):
        print("ServeRmore 0.0.3")

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
            return yaml.load(stream, Loader=yaml.FullLoader)

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

    bash$: srm help | settings | version
        - utility helpers
    bash$: srm lambda init | list
        - Set your runtime layers or list existing functions
    bash$: srm lambda create | update | destroy
        - Create your function, update it, or destroy it
    bash$: srm lambda invoke
        - Run your function from the command line\n\n"""
        print(s)

    def reset(self):
        return yaml.load("""
        aws:
            s3_bucket:
            s3_key:
        lambda:
            name:
            r_version: 3.5.3
            arn_role:
            arn_runtime_layer:
            arn_custom_layer:
            zip_file_name: lambda.zip
        """)
