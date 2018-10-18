#!/usr/bin/env python

import ctypes, os, io, yaml
from pathlib import Path

class CloudConfig:

    def __init__(self):
        # if config doesn't exist, copy over new one
        self.file = str(Path.home())+"/.serve-R-less.yaml"
        self.settings = {}
        self.pwd = os.getcwd()
        os.chdir(str(Path.home())+"/")
        self.load_all()
        self.set("aws", "base_dir", os.getcwd())

    def ask(self, compute_type):
        # Check for all values in yaml
        if not "repo" in self.settings["git"] or not self.settings["git"]["repo"]:
            git_repo = input("Please provide your Github Repo. (format: git@github.com:Origent/r-on-serverless.git)\n SSH URL: ")
            if not git_repo:
                git_repo = "git@github.com:Origent/r-on-serverless.git"
            self.set("git", "repo", git_repo)
        if not "private_key" in self.settings["git"] or not self.settings["git"]["private_key"]:
            git_private_key = input("Please provide the name of your Git Repo Private Key in ~/.ssh. (default: github.pem)\n KEY NAME: ")
            if not git_private_key:
                git_private_key = "github.pem"
            self.set("git", "private_key", git_private_key)
        if not "private_key" in self.settings["aws"] or not self.settings["aws"]["private_key"]:
            aws_private_key = input("Please provide the name of your Github Private Key stored in ~/.ssh. (default: aws.pem)\n KEY NAME: ")
            if not aws_private_key:
                aws_private_key = "aws.pem"
            self.set("aws", "private_key", aws_private_key)
        if compute_type == "builder":
            if not "lambda_handler_path" in self.settings["builder"] or not self.settings["builder"]["lambda_handler_path"]:
                py_handler_path = input("Please provide the path to your AWS Lambda handler.py function\n FILE PATH NAME: ")
                self.set("builder", "lambda_handler_path", py_handler_path)
            if not "lambda_function_name" in self.settings["builder"] or not self.settings["builder"]["lambda_function_name"]:
                api_function_name = input("Please provide the AWS Lambda function name that we will update. \n AWS Lambda Function Name: ")
                self.set("builder", "lambda_function_name", api_function_name)
            if not "lambda_s3_bucket" in self.settings["builder"] or not self.settings["builder"]["lambda_s3_bucket"]:
                s3_lambda_bucket = input("Please provide the AWS S3 Bucket name hosting the Lambda package. \n AWS Lambda S3 Bucket: ")
                self.set("builder", "lambda_s3_bucket", s3_lambda_bucket)
            if not "lambda_s3_key" in self.settings["builder"] or not self.settings["builder"]["lambda_s3_key"]:
                s3_lambda_key = input("Please provide the AWS S3 folder path and file name excluding the bucket name. \n AWS Lambda S3 Folder path & filename: ")
                self.set("builder", "lambda_s3_key", s3_lambda_key)

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
