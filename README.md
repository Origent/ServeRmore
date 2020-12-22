# ServeRmore

To help make R more accessible on Serverless Cloud Hosting, starting with AWS Lambda.
Python Package Index Releases: https://pypi.org/project/serveRmore/

## Requirements

Please refer to our [LAPTOP.md Guide](https://github.com/Origent/ServeRmore/blob/master/LAPTOP.md) for necessary manual configurations.

Please refer to your cloud platform for additional information:
* [AWS Lambda](AWS.md)

To install the latest package:
```
python3 -m pip install serveRmore
```

## Quickstart

1. Initiate your config file by typing "srm" or "srm help". These commands are available for awareness.  
```
srm help
srm version
srm status
```

2. At minimum for publishing function code, you'll need the following filled out in your ~/serveRmore.yaml file:
```
function:
  name:
  zip_file_name: null
  runtime: provided.al2
  arn_role: arn:aws:iam::<AWS_ID>:role/lambda_basic_execution
  arn_runtime_layer: arn:aws:lambda:us-east-1:<AWS_ID>:layer:<name>:<version>
  arn_custom_layer: arn:aws:lambda:us-east-1:<AWS_ID:layer:<name>:<version>
  s3_bucket:
  s3_key:
```

3. Create a new lambda.R script and create a "handler" method in R.  Insert "hello world" or custom code inside your handler method.

4. Create a new deploy.R script that will zip up your lambda.R and place on your AWS S3 bucket and key.

5. To deploy your zip file directly to Lambda, try out our new workflow here.
```
srm lambda create
srm lambda update
srm lambda invoke
srm lambda destroy
```

NOTE: 'create' will establish a brand new Lambda function if it does not exist, and publish your zip file.  'update' will republish your zip file, if your lambda function already exists.  

## Custom R Runtime Layers

To use additional R custom runtime layers that are prebuilt, or to help you build your own, refer to this guide: [R Runtime Custom Layers](custom_layer/README.md)

## Roadmap

v0.1.1
* Create more automation on custom layer building
    - Introduce custom layer settings from config file
    - Build & publish new layer
    - Save the ARN of the new layer to config

## Changelog

v0.1.0 - Removed original and deprecated deployment steps for custom Lambda packages that used r2py, Python 2, and R 3.4.2. Added new lambda layer builder VM commands.  Also migrated scripts for R, R-runtime, and R-gbm layers into subfolder for local Macbook environment.

v0.0.2 - Introduces running R directly on Lambda via AWS' new custom layers feature, big thanks to [@bakdata](https://github.com/bakdata).
* Several new commands for initiating the R runtime version, creating new functions, updating them, and destroying them.
* New documentation for how to build a custom R layer.

v0.0.1 - Initial Release
* Automated a genomics analysis guide that used Lambda with R.  Introduces an automated build process that creates a temporary AWS EC2 Virtual Machine, installs an R environment with CRAN and custom R packages, wraps them into a Lambda Package.  Also requires manual development of a Handler.py file that calls the R environment and R methods through r2py.
* Provides an easy way to iterate and repackage after handler.py changes.

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
