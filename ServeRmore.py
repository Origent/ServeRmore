#!/usr/bin/env python

import sys, time, srvl_config, VERSION
from signal import signal, SIGINT
from sys import exit

class srm:

    def __init__(self):
        self.cc = srvl_config.srvlConfig()

    def lambda_list(self):
        import boto3
        client = boto3.client('lambda')
        response = client.list_functions(
            MaxItems=50
        )
        for res in response["Functions"]:
            print(res["FunctionName"])

    def lambda_create(self):
        import boto3
        client = boto3.client('lambda')
        response = client.create_function(
            FunctionName=self.cc.settings["function"]["name"],
            Runtime=self.cc.settings["function"]["runtime"],
            Role=self.cc.settings["function"]["arn_role"],
            Handler='lambda.handler',
            Code={
                'S3Bucket': self.cc.settings["function"]["s3_bucket"],
                'S3Key': self.cc.settings["function"]["s3_key"]+"/"+self.cc.settings["function"]["zip_file_name"]
            },
            Timeout=60,
            MemorySize=3008,
            Layers=[
                self.cc.settings["function"]["arn_runtime_layer"],
                self.cc.settings["function"]["arn_custom_layer"]
            ]
        )

    def lambda_invoke(self):
        import boto3
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=self.cc.settings["function"]["name"]
        )

    def lambda_update(self):
        import boto3
        client = boto3.client('lambda')
        response = client.update_function_code(
            FunctionName=self.cc.settings["function"]["name"],
            S3Bucket=self.cc.settings["function"]["s3_bucket"],
            S3Key=self.cc.settings["function"]["s3_key"]+"/"+self.cc.settings["function"]["zip_file_name"]
        )

    def lambda_destroy(self):
        import boto3
        client = boto3.client('lambda')
        response = client.delete_function(
            FunctionName=self.cc.settings["function"]["name"]
        )

    def create(self):
        if not self.cc.settings["layers"]["instance_id"]:
            import boto3
            ec2 = boto3.resource('ec2')
            self.name_str = 'srm_layers_'+str(VERSION.srm_VERSION)
            instance = ec2.create_instances(
                BlockDeviceMappings=[{
                    'DeviceName': '/dev/xvda',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 50,
                        'VolumeType': 'gp2',
                    },
                },
                {
                    'DeviceName': '/dev/xvdcz',
                    'Ebs': {
                        'DeleteOnTermination': True,
                        'VolumeSize': 50,
                        'VolumeType': 'gp2',
                    },
                }],
                SecurityGroupIds=[
                    str(self.cc.settings["layers"]["ssh_security_group"]),
                    str(self.cc.settings["layers"]["default_security_group"])
                ],
                SubnetId=str(self.cc.settings["layers"]["subnet"]),
                ImageId=str(self.cc.settings["layers"]["ami"]),
                KeyName=str(self.cc.settings["layers"]["private_key"].replace('.pem', '')),
                MinCount=1,
                MaxCount=1,
                InstanceType=str(self.cc.settings["layers"]["instance_type"]),
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key':'Name',
                                'Value': self.name_str
                            }
                        ]
                    }
                ])
            print("Please wait for instance bootup.")
            time.sleep(5)
            self.cc.set("layers", "instance_id", instance[0].instance_id)
            print("New instance ID: " + self.cc.settings["layers"]["instance_id"])
            state = 'pending'
            while not state == 'running':
                time.sleep(5)
                instance = ec2.Instance(self.cc.settings["layers"]["instance_id"])
                state = instance.state["Name"]
                print("STATUS: "+state)
            time.sleep(1)
            self.cc.set("layers", "domain_name", instance.public_dns_name)
            print("Proceeding with bootstrapping instance.")
            self.bootstrap()
        else:
            print("Instance already exists.")

    def status(self):
        if self.cc.settings["layers"]["instance_id"]:
            import boto3
            resource = boto3.resource('ec2')
            instance = resource.Instance(self.cc.settings["layers"]["instance_id"])
            state = instance.state["Name"]
            print("Instance is "+ state + ".")
        else:
            print("No instance is allocated.")

    def cpu(self):
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["layers"]["private_key"], self.cc.settings["layers"]["domain_name"])
        cloud_connect.run_ssh(
            "printf '\nCPU core usage:' && " \
            "mpstat -P ALL 1 1 | awk '/Average:/ && $2 ~ /[0-9]/ {print $3\"%\"}' &&" \
            "printf 'Memory used:' &&" \
            "free -m | awk 'NR==2{print int($3*100/$2)\"%\" }' && " \
            "printf 'Storage used:' &&" \
            "df -h | awk '$NF==\"/\"{print $5}'")
        cloud_connect.terminate_ssh()

    def terminate(self):
        if input("are you sure? (y/n) ") == "y":
            if self.cc.settings["layers"]["instance_id"]:
                import boto3
                ec2 = boto3.resource('ec2')
                instance = ec2.Instance(self.cc.settings["layers"]["instance_id"])
                response = instance.terminate()
                self.cc.set("layers", "instance_id", '')
                self.cc.set("layers", "domain_name", '')
                print("Instance has been terminated.")
            else:
                print("No instance is running.")
                return False

    def ssh(self):
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.evoke_ssh('ec2-user',self.cc.settings["layers"]["domain_name"])

    def bootstrap(self):
        self.vm_setup()

    def vm_setup(self):
        from pathlib import Path
        print("Setting up VM for Lambda Layer Build Container...")
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["layers"]["private_key"], self.cc.settings["layers"]["domain_name"])
        print("Updating the VM...")
        cloud_connect.run_ssh("sudo yum -y update")
        cloud_connect.run_ssh("sudo yum -y install nfs-utils sysstat python3-setuptools")
        cloud_connect.run_ssh("pip3 install awscli --upgrade --user")
        cloud_connect.run_ssh("sudo yum -y -q install git nano zip")
        cloud_connect.upload_file_ssh(str(Path.home())+'/', '/home/ec2-user/', '.gitconfig')
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/.aws")
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'credentials')
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'config')
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/.ssh")
        cloud_connect.upload_file_ssh(str(Path.home())+'/.ssh/', '/home/ec2-user/.ssh/', self.cc.settings["git"]["private_key"])
        cloud_connect.run_ssh("echo 'IdentityFile ~/.ssh/github.pem' > /home/ec2-user/.ssh/config")
        cloud_connect.run_ssh("sudo chmod -R go-rwx /home/ec2-user/.ssh/")
        cloud_connect.run_ssh("ssh-keyscan -H github.com >> /home/ec2-user/.ssh/known_hosts")
        cloud_connect.run_ssh("git clone git@github.com:Origent/ServeRmore.git")
        cloud_connect.terminate_ssh()

    def restart_docker_service(self):
        print("Restart Docker Service...")
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["layers"]["private_key"], self.cc.settings["layers"]["domain_name"])
        cloud_connect.run_ssh("sudo service docker start")
        cloud_connect.terminate_ssh()
        print("Docker Service restarted...")
