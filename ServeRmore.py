#!/usr/bin/env python

import sys, time, srvl_config, srvl_connect, VERSION
from signal import signal, SIGINT
from sys import exit

class srm:

    def __init__(self):
        self.cc = srvl_config.srvlConfig()

    def lambda_init(self):
        import boto3
        my_session = boto3.session.Session()
        my_region = my_session.region_name
        client = boto3.client('lambda')
        response = client.list_layer_versions(
            LayerName='arn:aws:lambda:'+my_region+':131329294410:layer:r-runtime-'+self.cc.settings["lambda"]["r_version"].replace(".", "_"),
            MaxItems=1
        )
        print(response["LayerVersions"][0]["LayerVersionArn"])
        self.cc.set("lambda", "arn_runtime_layer", response["LayerVersions"][0]["LayerVersionArn"])

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
            FunctionName=self.cc.settings["lambda"]["name"],
            Runtime='provided',
            Role=self.cc.settings["lambda"]["arn_role"],
            Handler='lambda.handler',
            Code={
                'S3Bucket': self.cc.settings["aws"]["s3_bucket"],
                'S3Key': self.cc.settings["aws"]["s3_key"]+"/"+self.cc.settings["lambda"]["zip_file_name"]
            },
            Timeout=60,
            MemorySize=3008,
            Layers=[
                self.cc.settings["lambda"]["arn_runtime_layer"],
                self.cc.settings["lambda"]["arn_custom_layer"]
            ]
        )

    def lambda_invoke(self):
        import boto3
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=self.cc.settings["lambda"]["name"]
        )

    def lambda_update(self):
        import boto3
        client = boto3.client('lambda')
        response = client.update_function_code(
            FunctionName=self.cc.settings["lambda"]["name"],
            S3Bucket=self.cc.settings["aws"]["s3_bucket"],
            S3Key=self.cc.settings["aws"]["s3_key"]+"/"+self.cc.settings["lambda"]["zip_file_name"]
        )

    def lambda_destroy(self):
        import boto3
        client = boto3.client('lambda')
        response = client.delete_function(
            FunctionName=self.cc.settings["lambda"]["name"]
        )
    
    def create(self, name):
        if not self.cc.settings["rs"]["instance_id"]:
            import boto3
            ec2 = boto3.resource('ec2')
            self.name_str = 'srm_'+str(VERSION.VERSION)+'_rs_'+str(name)
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
                    str(self.cc.settings["aws"]["ssh_security_group"]),
                    str(self.cc.settings["aws"]["default_security_group"])
                ],
                SubnetId=str(self.cc.settings["aws"]["subnet"]),
                ImageId=str(self.cc.settings["rs"]["ami"]),
                KeyName=str(self.cc.settings["aws"]["private_key"].replace('.pem', '')),
                MinCount=1,
                MaxCount=1,
                InstanceType=str(self.cc.settings["rs"]["instance_type"]),
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
            self.cc.set("rs", "instance_id", instance[0].instance_id)
            print("New instance ID: " + self.cc.settings["rs"]["instance_id"])
            state = 'pending'
            while not state == 'running':
                time.sleep(5)
                instance = ec2.Instance(self.cc.settings["rs"]["instance_id"])
                state = instance.state["Name"]
                print("STATUS: "+state)
            time.sleep(1)
            self.cc.set("rs", "domain_name", instance.public_dns_name)
            print("Proceeding with bootstrapping instance.")
            self.bootstrap()
        else:
            print("Instance already exists.") 
    
    def status(self):
        if self.cc.settings["rs"]["instance_id"]:
            import boto3
            resource = boto3.resource('ec2')
            instance = resource.Instance(self.cc.settings["rs"]["instance_id"])
            state = instance.state["Name"]
            print("Instance is "+ state + ".")
        else:
            print("No instance is allocated.")
    
    def cpu(self):
        cloud_connect = srvl_connect.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
        cloud_connect.run_ssh(
            "printf '\nCPU core usage:' && " \
            "mpstat -P ALL 1 1 | awk '/Average:/ && $2 ~ /[0-9]/ {print $3\"%\"}' &&" \
            "printf 'Memory used:' &&" \
            "free -m | awk 'NR==2{print int($3*100/$2)\"%\" }' && " \
            "printf 'Storage used:' &&" \
            "df -h | awk '$NF==\"/\"{print $5}'")
        cloud_connect.terminate_ssh()
    
    def change(self):
        if self.cc.settings["rs"]["instance_id"]:
            import boto3
            client = boto3.client('ec2')
            self.cc.ask_new_instance_type("rs")
            print("Stopping the current instance...")
            client.stop_instances(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            waiter = client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            print("Modifying the current instance...")
            client.modify_instance_attribute(InstanceId=self.cc.settings["rs"]["instance_id"], Attribute='instanceType', Value=self.cc.settings["rs"]["instance_type"])
            print("Starting the current instance...")
            client.start_instances(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            waiter = client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(self.cc.settings["rs"]["instance_id"])
            self.cc.set("rs", "domain_name", instance.public_dns_name)
            cloud_connect = srvl_connect.srvlConnect()
            cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
            cloud_connect.run_ssh("sudo service docker restart")
            cloud_connect.run_ssh("sudo service ecs start")
            cloud_connect.run_ssh("docker start rstudio")
            cloud_connect.terminate_ssh()
            time.sleep(20)
            print("Successfully changed the instance type.  Please note the instance domain name for SSH has changed.")
        else:
            print("Successfully changed the default instance type.")
    
    def start(self):
        if self.cc.settings["rs"]["instance_id"]:
            import boto3
            client = boto3.client('ec2')
            print("Starting the current instance...")
            client.start_instances(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            waiter = client.get_waiter('instance_running')
            waiter.wait(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(self.cc.settings["rs"]["instance_id"])
            self.cc.set("rs", "domain_name", instance.public_dns_name)
            cloud_connect = srvl_connect.srvlConnect()
            cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
            cloud_connect.run_ssh("sudo service docker restart")
            cloud_connect.run_ssh("sudo service start ecs")
            cloud_connect.run_ssh("docker start rstudio")
            cloud_connect.terminate_ssh()
            time.sleep(20)
            print("Instance started. Please note the DNS and IP have changed.")
        else:
            print("No instance is stopped.")
            return False
            
    def stop(self):
        if self.cc.settings["rs"]["instance_id"]:
            import boto3
            client = boto3.client('ec2')
            ec2 = boto3.resource('ec2')
            instance = ec2.Instance(self.cc.settings["rs"]["instance_id"])
            state = instance.state["Name"]
            if state == "running":
                print("Stopping the current instance...")
                client.stop_instances(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
                waiter = client.get_waiter('instance_stopped')
                waiter.wait(InstanceIds=[self.cc.settings["rs"]["instance_id"]])
                print("Instance stopped.")
            else:
                print("Instance is already stopped.")
        else:
            print("No instance is running.")
            return False
    
    def terminate(self):
        if input("are you sure? (y/n) ") == "y":
            if self.cc.settings["rs"]["instance_id"]:
                import boto3
                ec2 = boto3.resource('ec2')
                instance = ec2.Instance(self.cc.settings["rs"]["instance_id"])
                response = instance.terminate()
                self.cc.set("rs", "instance_id", '')
                self.cc.set("rs", "domain_name", '')
                print("Instance has been terminated.")
            else:
                print("No instance is running.")
                return False
    
    def ssh(self):
        cloud_connect = srvl_connect.srvlConnect()
        cloud_connect.evoke_ssh('ec2-user',self.cc.settings["rs"]["domain_name"])
    
    def tunnel(self):
        cloud_connect = srvl_connect.srvlConnect()
        signal(SIGINT, int_handler)
        cloud_connect.evoke_multitunnel("-L 8787:"+self.cc.settings["rs"]["domain_name"]+":8787",'ec2-user@'+self.cc.settings["rs"]["domain_name"], self.cc.settings["aws"]["private_key"])
    
    def bootstrap(self):
        self.vm_setup()
        self.mount_efs_storage()
        self.restart_docker_service()
    
    def vm_setup(self):
        from pathlib import Path
        print("Setting up VM for RStudio Docker Container...")
        cloud_connect = srvl_connect.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
        print("Updating the VM...")
        cloud_connect.run_ssh("sudo yum -y update")
        cloud_connect.run_ssh("sudo yum -y install nfs-utils sysstat python3-setuptools")
        cloud_connect.run_ssh("pip3 install awscli --upgrade --user")
        cloud_connect.upload_file_ssh(str(Path.home())+'/', '/home/ec2-user/', '.gitconfig')
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/.ssh")
        cloud_connect.run_ssh("mkdir -p /home/ec2-user/.aws")
        cloud_connect.upload_file_ssh(str(Path.home())+'/.ssh/', '/home/ec2-user/.ssh/', self.cc.settings["git"]["private_key"])
        cloud_connect.upload_file_ssh(str(Path.home())+'/.ssh/', '/home/ec2-user/.ssh/', 'config')
        cloud_connect.upload_file_ssh(str(Path.home())+'/.ssh/', '/home/ec2-user/.ssh/', self.cc.settings["aws"]["private_key"])
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'credentials')
        cloud_connect.upload_file_ssh(str(Path.home())+'/.aws/', '/home/ec2-user/.aws/', 'config')
        cloud_connect.run_ssh("ssh-keyscan -H github.com >> /home/ec2-user/.ssh/known_hosts")
        cloud_connect.run_ssh("touch /home/ec2-user/.Renviron")
        cloud_connect.run_ssh("echo OPENSSL_CONF=/etc/ssl/ | tee -a /home/ec2-user/.Renviron")
        cloud_connect.terminate_ssh()
    
    def mount_efs_storage(self):
        cloud_connect = srvl_connect.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
        if "mount_efs" in self.cc.settings["aws"] and self.cc.settings["aws"]["mount_efs"]:
            print("connecting to AWS EFS storage.")
            cloud_connect.run_ssh("sudo mkdir -p /efs")
            cloud_connect.run_ssh("echo 'fs-921c01db.efs.us-east-1.amazonaws.com:/ /efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 0 0' | sudo tee -a /etc/fstab")
            cloud_connect.run_ssh("sudo mount -a")
            cloud_connect.run_ssh("sudo service ecs stop")
            cloud_connect.run_ssh("sudo service docker restart")
            cloud_connect.run_ssh("sudo service ecs start")
            cloud_connect.run_ssh("if grep /efs /proc/mounts; then echo 'EFS mount succeeded.'; else echo 'EFS mount failed.'; fi")
        cloud_connect.terminate_ssh()
    
    def restart_docker_service(self):
        print("Restart Docker Service...")
        cloud_connect = srvl_connect.srvlConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["rs"]["domain_name"])
        cloud_connect.run_ssh("sudo service docker start")
        cloud_connect.terminate_ssh()
        print("Docker Service restarted...")
