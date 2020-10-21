#!/usr/bin/env python

import sys, time, srvl_config, srvl_connect

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
