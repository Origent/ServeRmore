# ServeRmore

To help make R more accessible on Serverless Cloud Hosting, mainly with AWS Lambda.
Python Package Index Releases: [https://pypi.org/project/serveRmore/](https://pypi.org/project/serveRmore/)

## Prerequisites

Before this utility can be used, there are a number of assumptions made about your AWS environment. If you have a master account or your IAM account is provided full admin permissions, you can skip over the permissions section.

Permissions:
  * Can create and terminate EC2 instances
  * Can create API Gateways & Modify them
  * Can create Lambda Functions & Modify them
  * Can create S3 Buckets & Modify them
  
Also, if you do not already have a Base R Runtime Layer for your new Lambda Function, you'll need to build your own to use before your new Function will work. Some knowledge of AWS EC2 and AWS Cloud Networking is required in order to build a layer using the scripts provided. 

## Requirements

Please refer to the [LAPTOP.md Guide](LAPTOP.md) for necessary manual configurations.

To install the latest package:
```
python3 -m pip install serveRmore
```
### For Layer Building Only

In addition to the utility, if you plan to create your own R base Runtime Layer as well, you'll need to clone the entire repository locally:
```
git clone git@github.com:Origent/ServeRmore.git
```

**Note:**: We have used the following repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime

## Setup

Create a new file called "**serveRmore.yaml**" in your home directory. The template for the YAML file is shown below:  

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
* `s3_bucket`: storage bucket name for temporary function and layer zip files used to publish to Lambda Service.
* `s3_key`: the directory path within the bucket
* `arn`: "ARN" address for a configured runtime layer 

Additional Settings for Building the Layer:

* `ami`: The Amazon Machine Image ID. The specific one listed above is required, as it uses Amazon Linux 2 operating system with the Docker agent pre-installed.  Our scripts will pull from DockerHub.
* `default_security_group`: When creating an EC2 virtual machine instance, a security group is created automatically.  We recommend creating your own, or grabbing an existing security group ID and using that as your default here.  A security group is similar to a firewall, but is wrapped around a group of instances. 
* `ssh_security_group`: In order for the scripts to work, SSH must be enabled and reachable with the new Virtual Machine the build script creates. We recommend creating a new security group and allowing SSH port 22 inside the security group, and recording the ID here.
* `subnet`: When creating an EC2 virtual machine instance, it is added to a subnet and provided an IP address.  The subnets list can be found in the EC2 console.  Add the ID to one of them here.
* `instance_type`: The type determines cost and capability of the virtual machine.  The type provided has been tested, but many others could potentially work.
* `instance_id`: After the build script creates the virtual machine, the virtual machine Instance ID will be automatically placed here.
* `domain_name`: After the build script creates the virtual machine, the domain name of the VM will be automatically placed here.
* `private_key`: SSH key for AWS EC2 (see step 3 of the [LAPTOP.md Guide](LAPTOP.md))

## Function Deployments

1. Create a new **lambda.R** script and create a `handler` method in R.  Insert "hello world" or custom code inside your handler method.

2. Try out the SRM utility with any of these commands:

```
srm help
srm version
srm status
```

3. Create a new **deploy.R** script to do the following: (1) generate a zipped file containing your **lambda.R** script (and other helper scripts required by the function) and (2) upload the zipped file to the S3 directory specified by the `s3_bucket` and `s3_key` parameters in the YAML file. 

4. To deploy your zip file directly to Lambda, try out our new workflow here.
```
srm lambda create
srm lambda update
srm lambda invoke
srm lambda destroy
```

**Note**: `create` will establish a brand new Lambda function, if it does not exist, and publish your zip file;  `update` will republish your zip file, if your lambda function already exists.  

## Base R Runtime Layer Deployments

If you don't already have an R Runtime layer, you'll have to create your own before you can get your function code to run. We provide instructions for creating an R base Runtime Layer only, with intention to improve our scripts and instructions to include multiple layers.  If all is setup correctly from the additional settings above, all the heavy lifting is done! Building and Publishing the new R runtime layer only requires running three commands and waiting for them to complete.  

```
srm create
srm deploy
srm terminate
```

Double check the AWS Lambda Console and Layers registry as well as your **serveRmore.yaml** file to confirm that your layer was indeed published.

The following is included and required for the Runtime to work:
R 4.0.2 - In theory, all builds of 4.x should work, but only 4.0.2 has been tested.
httr - Used to communicate with other web APIs.
jsonlite - Used to load, parse, and create JSON documents.
aws.s3 - Used to interact with AWS S3 storage buckets.
logging - Used to help create well formed log streams.
yaml - Used to set configuration settings in a standardized way.

**Note:**: The build and compilation process uses a Docker image called [docker-lambda](https://github.com/lambci/docker-lambda).

### Base R Runtime Layer Debugging

If there are challenges with the layer build, there are ways to enter into an interactive mode. First, make sure that 'srm deploy' has already been run once, and that there is a VM running.  Entering 'srm status' will indicate status. Next, enter 'srm ssh', to login to the VM itself.  Then use the following command to login to the Docker container terminal itself:

```
docker run -it lambda-r:build-4.0.2 bash
```

There's a way to see which shared libraries are being used in the build environment by running  the following command to get a list:
```
ldd /opt/R/bin/exec/R
```

There's also a way to introduce print log statements int the Lambda R Runtime layer that will add log entries into AWS CloudWatch from AWS Lambda.  Once inside the Docker container, change directories and view the following file:
```
ServeRmore/layer/r-runtime/build/layers/r-runtime/build/layer/R/library/base/R/Rprofile
```
Then browse until you encounter the following function:
```
.First.sys()
```

Next, enter any of the following print statements, or enter your own:
```
print(paste0("PATH = ", Sys.getenv("PATH")))
print(paste0("Listing files in PATH /usr/local/bin:", paste(list.files("/usr/local/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /usr/bin/:", paste(list.files("/usr/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /bin:", paste(list.files("/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /opt/bin", paste(list.files("/opt/bin/"), collapse = ",")))
print(paste0("R.home() = ", file.path(R.home())))
print(paste0("Listing files in ", file.path(R.home(), "library"), ":", paste(list.files(file.path(R.home(), "library")), collapse = ",")))
```

Finally, exit the Docker container, and while still in the VM, execute the Deploy.sh script:
```
./deploy.sh
```

Your new R Runtime Layer should now be published with your print statements.

### Base R Runtime Layer Limitations

AWS Lambda is limited to running with 3GB RAM and must finish within 15 minutes. It is therefore not feasible to execute long running R scripts with this runtime. Furthermore, only the `/tmp/` directory is writeable on AWS Lambda. This must be considered when writing to the local disk.

## Creating your own Layer

If you decide to create your own layer, here's a few things to think about and a few steps to help you get started.

1. There is a current limit of 5 layers that a Lambda Function can have.
2. The Lambda Layer zip package has size limits. For example, it is extremely unlikely to be able to package up the entire Tidyverse as a layer. This could change as the AWS Lambda Service changes its requirements.  
3. The more that is added to the layer, the slower the function performance will become, as it will be spending more time starting up the environment to run the function code.  
4. Precision is important. Unlike an R&D or exploratory programming environment, each decision has an impact on functionality, performance, and quality.

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
