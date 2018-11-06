#!/usr/bin/env python

import time, paramiko
from pathlib import Path

class srvlConnect:

    def evoke_ssh(self, user_name, domain_name, remote_port=22):
        import subprocess
        import sys
        COMMAND="ssh "+ user_name + "@" + domain_name + " -o TCPKeepAlive=yes -o ServerAliveInterval=50 -p " + str(remote_port)
        result = subprocess.call(COMMAND,shell=True)

    def evoke_sftp(self, user_name, domain_name, remote_port=22):
        import subprocess
        import sys
        COMMAND="sftp "+ user_name + "@" + domain_name + " -o TCPKeepAlive=yes -o ServerAliveInterval=50 -p " + str(remote_port)
        result = subprocess.call(COMMAND,shell=True)

    def evoke_tunnel(self, user_name, domain_name, remote_port, local_port, private_key):
        import subprocess
        import sys
        COMMAND="ssh -i ~/.ssh/"+private_key+" -F ~/.ssh/config -N -L "+str(local_port)+":"+domain_name+":"+str(remote_port)+" "+user_name+"@"+ domain_name + " -o TCPKeepAlive=yes -o ServerAliveInterval=50 -o ExitOnForwardFailure=yes"
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

    def download_file_ssh(self, remote_path, local_path, value):
        sftp = self.client.open_sftp()
        print("copying from: "+remote_path+value)
        print("copying to: "+local_path+value)
        sftp.put(remote_path+value, local_path+value)

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

    def copy_to_s3(self, local_path, remote_path):
        import subprocess
        import sys
        COMMAND="aws s3 cp "+ local_path + " " + remote_path
        result = subprocess.call(COMMAND,shell=True)

    def copy_from_s3(self, local_path, remote_path):
        import subprocess
        import sys
        COMMAND="aws s3 cp " + remote_path + " " + local_path
        result = subprocess.call(COMMAND,shell=True)
