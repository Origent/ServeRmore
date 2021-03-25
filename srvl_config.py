#!/usr/bin/env python

import ctypes, os, io, yaml, time, paramiko, VERSION
from pathlib import Path
from setuptools import setup

class srvlConfig:

    def __init__(self):
        self.file = str(Path.home())+"/serveRmore.yaml"
        self.settings = {}
        self.pwd = os.getcwd()
        os.chdir(str(Path.home())+"/")
        self.load_all()

    def show(self):
        if not self.exists():
            return False
        else:
            print(yaml.dump(self.load(), default_flow_style=False))

    def set_env(self, env_str):
        self.settings["env"] = env_str
        with io.open(self.file, 'w', encoding='utf8') as outfile:
            yaml.dump(self.settings, outfile, default_flow_style=False, allow_unicode=True)

    def version(self):
        print("ServeRmore "+VERSION.srm_VERSION)

    def load_all(self):
        self.settings = self.load()

    def write_all(self):
        for key in self.settings:
            for name in self.settings[key]:
                self.write(key,name, self.settings[key][name])

    def set(self, key, name, value):
        if key == "build_vm":
            self.settings[key][name] = value
            self.write(key,name,value)
        else:
            env = self.settings["env"]
            self.settings[env][key][name] = value
            with io.open(self.file, 'w', encoding='utf8') as outfile:
                yaml.dump(self.settings, outfile, default_flow_style=False, allow_unicode=True)

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
            raise ValueError("serveRmore.yaml configuration can not be found in your home directory.  Please refer to ServeRmore README instructions.")
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
    bash$: srm lambda list | create | update | destroy
        - List functions, create your function, update it, or destroy it
    bash$: srm create | deploy | terminate | ssh | cpu | status
        - Create and interact with your layer builder VM\n\n"""
        print(s)

class srvlConnect:

    def evoke_ssh(self, user_name, domain_name, remote_port=22):
        import subprocess
        import sys
        COMMAND="ssh "+ user_name + "@" + domain_name + " -o TCPKeepAlive=yes -o ServerAliveInterval=50 -p " + str(remote_port)
        result = subprocess.call(COMMAND,shell=True)

    def evoke_multitunnel(self, tunnel_str, connect_str, private_key):
        import subprocess
        import sys
        COMMAND="ssh -i ~/.ssh/"+private_key+" -F ~/.ssh/config -N " + tunnel_str + " " + connect_str + " -o TCPKeepAlive=yes -o ServerAliveInterval=50 -o ExitOnForwardFailure=yes"
        print("SSH Tunnel Connected - please type Ctrl-C to terminate.")
        result = subprocess.call(COMMAND,shell=True)

    def initiate_ssh(self,user,key,domain):
        self.user_name = user
        self.private_key = key
        self.domain_name = domain
        import paramiko
        from pathlib import Path
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        key_object = paramiko.RSAKey.from_private_key_file(str(Path.home())+"/.ssh/"+self.private_key)
        proceed = False
        while proceed == False:
            print("Attempting SSH connection...")
            try:
                self.client.connect(hostname=self.domain_name, port=22, username=self.user_name, pkey=key_object)
                proceed = True
                print("SSH successful!")
            except Exception as e:
                proceed = False
                print("SSH failed... temporary delay enabled.")
                time.sleep(5)
        self.session = self.client.get_transport().open_session()

    def run_ssh(self,cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        self.wait_for_command(stdout)

    def upload_file_ssh(self, local_path, remote_path, value):
        sftp = self.client.open_sftp()
        print("copying from: "+local_path+value)
        print("copying to: "+remote_path+value)
        sftp.put(local_path+value, remote_path+value)

    def terminate_ssh(self):
        self.client.close()

    def wait_for_command(self,stdout):
        import select
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    print(str(stdout.channel.recv(1024), 'utf-8').replace('\\n', '\n'))

    def get_aws_access_key(self):
        import botocore.session
        return botocore.session.get_session().get_credentials().access_key

    def get_aws_secret_key(self):
        import botocore.session
        return botocore.session.get_session().get_credentials().secret_key

    def get_aws_region(self):
        import botocore.session
        return botocore.session.get_session().get_config_variable('region')
