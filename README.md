# ServeRmore

To help make R more accessible on Serverless Cloud Hosting, mainly with AWS Lambda.
Python Package Index Releases: [https://pypi.org/project/serveRmore/](https://pypi.org/project/serveRmore/)

## Requirements

Please refer to the [LAPTOP.md Guide](LAPTOP.md) for necessary manual configurations.

Please refer to your cloud platform for additional information:
* [AWS Lambda](AWS.md)

To install the latest package:
```
python3 -m pip install serveRmore
```

## Quickstart

1. Create a new file called "**serveRmore.yaml**" in your home directory. The template for the YAML file is shown below:  

```
aws:
  s3_bucket: null
  s3_key: null
function:
  arn_role: arn:aws:iam::<AWS_ID>:role/lambda_basic_execution
  handler: lambda.handler
  name: null
  zip_file_name: null
  runtime: provided.al2
runtime_layer:
  arn: arn:aws:lambda:us-east-1:<AWS_ID>:layer:<name>:<version>
  r_packages: httr logging yaml jsonlite aws.s3 
  r_version: 4.0.2
build_vm:
  ami: ami-02507631a9f7bc956
  default_security_group: null
  ssh_security_group: null
  subnet: null
  instance_type: t2.large
  domain_name: null
  instance_id: null
  private_key: null
```

For deploying a new Lambda function only (i.e. not including a Lambda _layer_), at the least you will need the following parameters: 

* `arn_role`: AWS Account ID 
* `handler`: path to the starting method call
* `name`: the name of the Lambda function
* `zip_file_name`: temporary zip file that contains the main script along with any helper scripts required by the function
* `private_key`: SSH key for AWS EC2 (see step 3 of the [LAPTOP.md Guide](LAPTOP.md))
* `s3_bucket`: storage for Lambda function script
* `arn`: "ARN" address for a configured runtime layer 

**Note:** If you do not have a runtime layer pre-configured, follow the instructions for layer building under the section "Custom R Runtime Layers". 

2. Create a new **lambda.R** script and create a `handler` method in R.  Insert "hello world" or custom code inside your handler method.

3. Try out the SRM utility with any of these commands:

```
srm help
srm version
srm status
```

4. Create a new **deploy.R** script to do the following: (1) generate a zipped file containing your **lambda.R** script (and other helper scripts required by the function) and (2) upload the zipped file to the S3 directory specified by the `s3_bucket` and `s3_key` parameters in the YAML file. 

5. To deploy your zip file directly to Lambda, try out our new workflow here.
```
srm lambda create
srm lambda update
srm lambda invoke
srm lambda destroy
```

**Note**: `create` will establish a brand new Lambda function, if it does not exist, and publish your zip file;  `update` will republish your zip file, if your lambda function already exists.  

## Custom R Runtime Layers

If you don't already have an R Runtime layer, you'll have to create your own before you can get your function code to run. To build your own runtime, refer to this guide: [R Runtime Custom Layers](layers/README.md)

## Roadmap

v0.1.1 - Additional Updates
* Add multi-layer support
* Remove the dependency of cloning the repo locally along with installing the utility to build layers

## Changelog

v0.1.0 - Revamped Lambda Service Layers and removed outdated deployment steps

* Added support for R v4.0.2 
* Simplified the layer building process and scripts
* Support for one custom runtime layer for R with customizable R packages
* Auto-Save of the ARN for new runtime layer 
* Removed reliance on r2py, Python 2, and R 3.4.2

v0.0.2 - Introduces running R directly on Lambda via new AWS custom layers feature, big thanks to [@bakdata](https://github.com/bakdata).

* Several new commands for initiating the R runtime version, creating new functions, updating them, and destroying them.
* New documentation for how to build a custom R layer.

v0.0.1 - Initial Release

* Automated a genomics analysis guide that used Lambda with R.  Introduces an automated build process that creates a temporary AWS EC2 Virtual Machine, installs an R environment with CRAN and custom R packages, wraps them into a Lambda Package.  Also requires manual development of a Handler.py file that calls the R environment and R methods through r2py.
* Provides an easy way to iterate and repackage after handler.py changes.

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
