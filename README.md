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

2. Update your config file in your home directory.  At minimum, you'll need:
  * Your own Lambda Execution Role 'arn' value.
  * An S3 bucket and an S3 bucket key (folder).
  * Lambda function name

3. Create a new lambda.R script and create a "handler" method in R.  Insert "hello world" or custom code inside your handler method.

4. Create a new package.R script that will zip up your lambda.R and place on your AWS S3 bucket and key.

5. To deploy your zip file directly to Lambda, try out our new workflow here.
```
srm lambda init
srm lambda create
srm lambda update
srm lambda invoke
srm lambda destroy
```

NOTE: 'init' will establish your R Runtime ARN value in your config.  'create' will establish a brand new Lambda function if it does not exist, and publish your zip file.  'update' will republish your zip file, if your lambda function already exists.  

## Custom R Runtime Layers

To use additional R custom runtime layers that are prebuilt, or to help you build your own, refer to this guide: [R Runtime Custom Layers](custom_layer/README.md)

We have an older way of deploying on Lambda that we still support for the time being.  You can learn more here: [R Environment in Python Runtime](deprecated.md)

## Roadmap

v0.1.0
* Create more automation on custom layer building
    - Revise ServeRmore.yaml config file for new configurations
    - Launch a temporary EC2 VM
    - Pull down the github repo from bakdata
    - Introduce custom layer settings from config file
    - Build & publish new layer
    - Save the ARN of the new layer to config
    - Terminate the VM
* Remove old EC2 Virtual Machine on Python runtime workflow

## Changelog

v0.0.2 - Introduces running R directly on Lambda via AWS' new custom layers feature, big thanks to [@bakdata](https://github.com/bakdata).
* Several new commands for initiating the R runtime version, creating new functions, updating them, and destroying them.
* New documentation for how to build a custom R layer.

v0.0.1 - Initial Release
* Automated a genomics analysis guide that used Lambda with R.  Introduces an automated build process that creates a temporary AWS EC2 Virtual Machine, installs an R environment with CRAN and custom R packages, wraps them into a Lambda Package.  Also requires manual development of a Handler.py file that calls the R environment and R methods through r2py.
* Provides an easy way to iterate and repackage after handler.py changes.

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
