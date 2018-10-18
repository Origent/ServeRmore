#!/usr/bin/env python

import sys, time, config, connect

class Builder:

    def __init__(self):
        self.cc = config.CloudConfig()
        self.cc.ask("builder")
        self.name_str = 'Lambda Builder'

    def create(self):
        import boto3
        self.name_str = str(name) + ' ' + str(self.name_str)
        prompt1_str = "New Lambda Builder ID: "
        prompt2_str = "Lambda Builder already exists."
        if not self.cc.settings["builder"]["vm_instance_id"]:
            ec2 = boto3.resource('ec2')
            instance = ec2.create_instances(
                SecurityGroupIds=[
                    str(self.cc.settings["aws"]["ssh_sec_group"]),
                ],
                SubnetId=str(self.cc.settings["aws"]["subnet"]),
                ImageId=str(self.cc.settings["builder"]["vm_ami"]),
                KeyName=str(self.cc.settings["aws"]["private_key"].replace('.pem', '')),
                MinCount=1,
                MaxCount=1,
                InstanceType=str(self.cc.settings["builder"]["vm_instance_type"]),
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key':'Name',
                                'Value': str(self.name_str)
                            }
                        ]
                    }
                ])
            print("Please wait for Builder bootup.")
            time.sleep(5)
            self.cc.set("builder", "vm_instance_id", instance[0].instance_id)
            print(prompt1_str + self.cc.settings["builder"]["vm_instance_id"])
            state = 'pending'
            while not state == 'running':
                time.sleep(5)
                instance = ec2.Instance(self.cc.settings["builder"]["vm_instance_id"])
                state = instance.state["Name"]
                print("STATUS: "+state)
            time.sleep(5)
            self.cc.set("builder", "vm_domain_name", instance.public_dns_name)
            self.cc.set("builder", "vm_public_ip", instance.public_ip_address)
            print("Proceeding with bootstrapping Builder.")
            time.sleep(20)
            self.bootstrap()
        else:
            print(prompt2_str)

    def status(self):
        if self.cc.settings["builder"]["vm_instance_id"]:
            import boto3
            client = boto3.client('ec2')
            response = client.describe_instance_status(
                Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': [
                            'running',
                        ]
                    },
                ],
                InstanceIds=[
                    self.cc.settings["builder"]["vm_instance_id"]
                ]
            )
            print(response)

        else:
            print("No Lambda Builder instance is running.")

    def terminate(self):
        if input("are you sure? (y/n) ") == "y":
            if self.cc.settings["builder"]["vm_instance_id"]:
                import boto3
                ec2 = boto3.resource('ec2')
                response = ec2.instances.filter(InstanceIds=[self.cc.settings["builder"]["vm_instance_id"]]).terminate()
                self.cc.set("builder", "vm_instance_id", '')
                self.cc.set("builder", "vm_domain_name", '')
                self.cc.set("builder", "vm_public_ip", '')
                print(response)
            else:
                return False

    def ssh(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.evoke_ssh('ec2-user',self.cc.settings["builder"]["vm_domain_name"])

    def sftp(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.evoke_sftp('ec2-user',self.cc.settings["builder"]["vm_domain_name"])

    def bootstrap(self):
        self.upload_aws()
        self.init_builder()
        self.init_pvenv()

    def upload_aws(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.run_ssh("pip install awscli --upgrade --user")
        cloud_connect.run_ssh("mkdir ~/.aws")
        cloud_connect.run_ssh("echo \"[default]\naws_access_key_id = "+cloud_connect.get_aws_access_key()+"\n"+
            "aws_secret_access_key = "+cloud_connect.get_aws_secret_key()+"\" > ~/.aws/credentials")
        cloud_connect.run_ssh("echo \"[default]\nregion = "+cloud_connect.get_aws_region()+"\" > .aws/config")
        cloud_connect.run_ssh("sudo cp -R /home/ec2-user/.aws /root/")
        cloud_connect.terminate_ssh()

    def init_builder(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.run_ssh("sudo yum -y update")
        cloud_connect.run_ssh("sudo yum -y upgrade")
        cloud_connect.run_ssh("sudo yum -y install python27-devel python27-pip gcc gcc-c++ readline-devel libgfortran.x86_64 R.x86_64")
        cloud_connect.run_ssh("pip install --upgrade pip")
        cloud_connect.upload_file_ssh(self.cc.settings["builder"]["py_handler_path"]+"/", '/home/ec2-user/', 'package_install.R')

        # Create package_install.R script
        # For loop to read in yaml R package names and install
        #  install.packages('', repos='http://cran.us.r-project.org')
        #
        
        cloud_connect.terminate_ssh()
        print("Running R Package Installs")
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.run_ssh("sudo Rscript package_install.R")
        print("Finished R Package Installs")
        cloud_connect.terminate_ssh()

    def init_pvenv(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.run_ssh("virtualenv $HOME/env && source $HOME/env/bin/activate && pip install 'rpy2<2.9.0'")
        cloud_connect.run_ssh("mkdir $HOME/packaging && cd $HOME/packaging")
        cloud_connect.run_ssh("sudo rm /usr/lib64/R/lib/libRrefblas.so")
        cloud_connect.run_ssh("cp -r /usr/lib64/R/* $HOME/packaging")
        cloud_connect.run_ssh("cp /usr/lib64/libgomp.so.1 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libgfortran.so.3 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libquadmath.so.0 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libm.so.6 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libreadline.so.6 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libtre.so.5 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libpcre.so.0 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/liblzma.so.5 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libbz2.so.1 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libz.so.1 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/librt.so.1 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libdl.so.2 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libicuuc.so.50 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libicui18n.so.50 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libgcc_s.so.1 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /lib64/libtinfo.so.5 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libicudata.so.50 $HOME/packaging/lib")
        cloud_connect.run_ssh("cp /usr/lib64/libstdc++.so.6 $HOME/packaging/lib")
        cloud_connect.run_ssh("virtualenv $HOME/env && source $HOME/env/bin/activate && cp -r $VIRTUAL_ENV/lib64/python2.7/dist-packages/* $HOME/packaging")
        cloud_connect.run_ssh("virtualenv $HOME/env && source $HOME/env/bin/activate && cp -r $VIRTUAL_ENV/lib/python2.7/dist-packages/singledispatch* $HOME/packaging")
        cloud_connect.run_ssh("cp $HOME/packaging/bin/exec/R $HOME/packaging")
        cloud_connect.terminate_ssh()

    def push_handler(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.upload_file_ssh(self.cc.settings["builder"]["lambda_handler_path"]+"/", "/home/ec2-user/packaging/", 'handler.py')
        cloud_connect.terminate_ssh()

    def package_to_s3(self):
        cloud_connect = connect.SSHConnect()
        cloud_connect.initiate_ssh("ec2-user", self.cc.settings["aws"]["private_key"], self.cc.settings["builder"]["vm_domain_name"])
        cloud_connect.run_ssh("cd $HOME/packaging/ && zip -r9 $HOME/lambda.zip *")
        cloud_connect.run_ssh("aws s3 cp $HOME/lambda.zip s3://"+
        self.cc.settings["builder"]["lambda_s3_bucket"]+"/"+self.cc.settings["builder"]["lambda_s3_key"])
        cloud_connect.terminate_ssh()

    def update_lambda(self):
        import boto3
        client = boto3.client('lambda')
        response = client.update_function_code(
            FunctionName=self.cc.settings["builder"]["lambda_function_name"],
            S3Bucket=self.cc.settings["builder"]["lambda_s3_bucket"],
            S3Key=self.cc.settings["builder"]["lambda_s3_key"],
        )
        print(response)
