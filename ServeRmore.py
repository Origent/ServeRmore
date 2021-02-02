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
            Handler=self.cc.settings["function"]["handler"],
            Code={
                'S3Bucket': self.cc.settings["aws"]["s3_bucket"],
                'S3Key': self.cc.settings["aws"]["s3_key"]+"/"+self.cc.settings["function"]["zip_file_name"]
            },
            Timeout=60,
            MemorySize=3008,
            Layers=[
                self.cc.settings["runtime_layer"]["arn"]
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
            S3Bucket=self.cc.settings["aws"]["s3_bucket"],
            S3Key=self.cc.settings["aws"]["s3_key"]+"/"+self.cc.settings["function"]["zip_file_name"]
        )

    def lambda_destroy(self):
        import boto3
        client = boto3.client('lambda')
        response = client.delete_function(
            FunctionName=self.cc.settings["function"]["name"]
        )

    def create(self):
        if not self.cc.settings["build_vm"]["instance_id"]:
            import boto3
            ec2 = boto3.resource('ec2')
            self.name_str = 'srm_R_layer_'+str(VERSION.srm_VERSION)
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
                    str(self.cc.settings["build_vm"]["ssh_security_group"]),
                    str(self.cc.settings["build_vm"]["default_security_group"])
                ],
                SubnetId=str(self.cc.settings["build_vm"]["subnet"]),
                ImageId=str(self.cc.settings["build_vm"]["ami"]),
                KeyName=str(self.cc.settings["build_vm"]["private_key"].replace('.pem', '')),
                MinCount=1,
                MaxCount=1,
                InstanceType=str(self.cc.settings["build_vm"]["instance_type"]),
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
            self.cc.set("build_vm", "instance_id", instance[0].instance_id)
            print("New instance ID: " + self.cc.settings["build_vm"]["instance_id"])
            state = 'pending'
            while not state == 'running':
                time.sleep(5)
                instance = ec2.Instance(self.cc.settings["build_vm"]["instance_id"])
                state = instance.state["Name"]
                print("STATUS: "+state)
            time.sleep(1)
            self.cc.set("build_vm", "domain_name", instance.public_dns_name)
            print("Proceeding with bootstrapping instance.")
            self.vm_setup()
        else:
            print("Instance already exists.")

    def deploy(self):
        if self.cc.settings["build_vm"]["instance_id"]:
            from pathlib import Path
            cloud_connect = srvl_config.srvlConnect()
            cloud_connect.initiate_ssh("ec2-user", self.cc.settings["build_vm"]["private_key"], self.cc.settings["build_vm"]["domain_name"])
            print("Running Build script for Lambda Layer...")
            cloud_connect.run_ssh("./build.sh " + self.cc.settings["runtime_layer"]["r_version"] +" \""+ str(self.cc.settings["runtime_layer"]["r_packages"]) + "\" 2>&1")
            print("Running Deploy script for Lambda Layer...")
            cloud_connect.run_ssh("./deploy.sh " + self.cc.settings["runtime_layer"]["r_version"] + " " + self.cc.settings["aws"]["s3_bucket"] + " " + self.cc.settings["aws"]["s3_key"] + " 2>&1")
            cloud_connect.terminate_ssh()
            import boto3
            client = boto3.client('lambda')
            response = client.list_layer_versions(
                LayerName='r-runtime-4_0_2'
            )
            print("Updating Published Version for Lambda Layer...")
            self.cc.set("runtime_layer", "arn", response["LayerVersions"][0]["LayerVersionArn"])
        else:
            print("No instance is allocated.")

    def status(self):
        if self.cc.settings["build_vm"]["instance_id"]:
            import boto3
            resource = boto3.resource('ec2')
            instance = resource.Instance(self.cc.settings["build_vm"]["instance_id"])
            state = instance.state["Name"]
            print("Instance is "+ state + ".")
        else:
            print("No instance is allocated.")

    def cpu(self):
        if self.cc.settings["build_vm"]["instance_id"]:
            cloud_connect = srvl_config.srvlConnect()
            cloud_connect.initiate_ssh("ec2-user", self.cc.settings["build_vm"]["private_key"], self.cc.settings["build_vm"]["domain_name"])
            cloud_connect.run_ssh(
                "printf '\nCPU core usage:' && " \
                "mpstat -P ALL 1 1 | awk '/Average:/ && $2 ~ /[0-9]/ {print $3\"%\"}' &&" \
                "printf 'Memory used:' &&" \
                "free -m | awk 'NR==2{print int($3*100/$2)\"%\" }' && " \
                "printf 'Storage used:' &&" \
                "df -h | awk '$NF==\"/\"{print $5}'")
            cloud_connect.terminate_ssh()
        else:
            print("No instance is allocated.")

    def terminate(self):
        if input("are you sure? (y/n) ") == "y":
            if self.cc.settings["build_vm"]["instance_id"]:
                import boto3
                ec2 = boto3.resource('ec2')
                instance = ec2.Instance(self.cc.settings["build_vm"]["instance_id"])
                response = instance.terminate()
                self.cc.set("build_vm", "instance_id", '')
                self.cc.set("build_vm", "domain_name", '')
                print("Instance has been terminated.")
            else:
                print("No instance is running.")
                return False

    def ssh(self):
        if self.cc.settings["build_vm"]["instance_id"]:
            cloud_connect = srvl_config.srvlConnect()
            cloud_connect.evoke_ssh('ec2-user',self.cc.settings["build_vm"]["domain_name"])
        else:
            print("No instance is allocated.")

    def vm_setup(self):
        from pathlib import Path
        print("Setting up VM for Lambda Layer Build Container...")
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["build_vm"]["private_key"], self.cc.settings["build_vm"]["domain_name"])
        print("Updating the VM...")
        cloud_connect.run_ssh("sudo yum -y update")
        cloud_connect.run_ssh("sudo yum -y install nfs-utils sysstat python3-setuptools")
        cloud_connect.run_ssh("pip3 install awscli --upgrade --user")
        cloud_connect.run_ssh("sudo yum -y -q install git nano zip")
        cloud_connect.upload_file_ssh(str(Path.home())+'/', '/home/ec2-user/', '.gitconfig')
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/.aws")
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'credentials')
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'config')
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/', '/home/ec2-user/', "Dockerfile")
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/', '/home/ec2-user/', "build.sh")
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/', '/home/ec2-user/', "deploy.sh")
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/src")
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/src/', '/home/ec2-user/src/', "bootstrap")
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/src/', '/home/ec2-user/src/', "bootstrap.R")
        cloud_connect.upload_file_ssh(str(Path.home())+'/ServeRmore/layers/src/', '/home/ec2-user/src/', "runtime.R")
        cloud_connect.run_ssh("chmod -R ugo+x build.sh deploy.sh ./src")
        cloud_connect.terminate_ssh()

    def restart_docker_service(self):
        print("Restart Docker Service...")
        cloud_connect = srvl_config.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["build_vm"]["private_key"], self.cc.settings["build_vm"]["domain_name"])
        cloud_connect.run_ssh("sudo service docker start")
        cloud_connect.terminate_ssh()
        print("Docker Service restarted...")
