## Custom R Runtime Layers

ToDo:


* Add step to pull Repo into VM

### Dependencies

* Install Docker Desktop on Mac or use an EC2 VM with the docker service installed.
* We have used the following repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime

### HowTo

You can build two layers from scratch.  Please take the following steps to complete.

1. Use the "srm" utility to create a new VM.  Then login to it.
```
srm create
srm ssh
```

2. Pull down the ServeRmore repo locally.
```
git clone git@github.com/Origent/ServeRmore.git
git fetch origin
git pull origin srm_0.1.0
```

3. We want to make sure that shell/terminal scripts are executable.
```
cd ServeRmore/layers
chmod u+rwx -R *.sh
chmod u+rwx -R r/*.sh
chmod u+rwx -R r-runtime/*.sh
chmod u+rwx -R r-gbm/*.sh
```

4. Double check several scripts to ensure they are correct for R v4.x or a newer version you might be working with.  Namely, the Dockerfile "ARG VERSION=x.x.x" variable and the 'wget' line, along with the r/compile.sh script 'wget' line.  They should say R-4 for 4.x.x versions of base R, as we are no longer working with R 3.x.x.

5. We will run the build script for the R base, R layer, and GBM layer. To build the layers yourself, you need to first build R from source. We provide a Docker image which uses the great [docker-lambda](https://github.com/lambci/docker-lambda) project. You can build R, R runtime layer, and R gbm layer all at once.  Just do the following with your version number and everything should be build properly.
```
./build.sh 4.0.2
```

6. We then run the deploy script for the R layer and GBM layer. This publishes to your AWS account if you have previously followed the LAPTOP setup guide and you have an active AWS account.

If you plan to publish the runtime and gbm layers, you need to have a recent version of aws cli (>=1.16). When you run the deploy script with your version number, it creates two lambda layers named `r-<layer>-<version>` in your AWS account.
```
./deploy.sh 4.0.2
```

### Debugging

If there are challenges with the layer build, the following command can be run in order to interact with the environment inside the docker service used to build the layer.
```
docker run -it lambci/lambda:build-provided.al2 bash
```

Once inside the Terminal of the Docker service, the individual commands listed in Dockerfile can be run.

### r-runtime layer

The r-runtime base layer has the following packages installed.

R,
[httr](https://cran.r-project.org/package=httr),
[jsonlite](https://cran.r-project.org/package=jsonlite),
[aws.s3](https://cran.r-project.org/package=aws.s3),
[logging](https://cran.r-project.org/package=logging),
[yaml](https://cran.r-project.org/package=yaml)

### r-gbm layer

The r-gbm base layer has the following packages installed.

[Matrix](https://cran.r-project.org/package=Matrix),
[survival](https://cran.r-project.org/package=survival)
[gridExtra](https://cran.r-project.org/package=gridExtra)
[lattice](https://cran.r-project.org/package=lattice)
[gbm](https://cran.r-project.org/package=gbm)

## Limitations

AWS Lambda is limited to running with 3GB RAM and must finish within 15 minutes. It is therefore not feasible to execute long running R scripts with this runtime. Furthermore, only the `/tmp/` directory is writeable on AWS Lambda. This must be considered when writing to the local disk.

## Creating your own Layer

If you decide to create your own layer, here's a few things to think about and a few steps to help you get started.

Concepting:
  1. Keep in mind the limits in how many layers a Lambda Function can have. I believe this remains a modest number.
  2. Keep in mind the Lambda Layer zip package size limits.  It is extremely unlikely to be able to package up the entire Tidyverse as a layer, for example.  This could change as the AWS Lambda Service changes its requirements.  
  3. Keep in mind, the more you add, the slower the Function performance will be come, as you'll be spending a lot more time starting up the environment to run the function code.  
  4. Precision is important.  Unlike an R&D or exploratory programming environment, each decision has an impact on functionality, performance, and quality.

Building:
  1. The r-gbm directory is the best example of a custom layer that assumes an equivalent R base is provided in a separate layer.
  2. Copy the directory under a new name, then find the two places where R packages are installed.  Swap out the package names for the packages you want in your new layer.
  3. Build the layer, publish it in your AWS Lambda console, and then publish a Function that depends on it, to test it out.  Repeat the process until you've proven it works successfully.  

### Compiling on EC2 (Don't Use - Not updated)

In case the Docker image does not properly represent the lambda environment,
we also provide a script which launches an EC2 instance, compiles R, and uploads the zipped distribution to S3.
You need to specify the R version, e.g., `3.6.3`, as well as the S3 bucket to upload the distribution to.
Finally, you need to create an EC2 instance profile which is capable of uploading to the S3 bucket.
See the [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html#create-iam-role) for details.
With everything prepared, you can run the script:
```bash
./remote_compile_and_deploy.sh <version> <bucket-name> <instance-profile>
```
The script will also take care of terminating the launched EC2 instance.

To manually build R from source, follow these steps:

Start an EC2 instance which uses the [Lambda AMI](https://console.aws.amazon.com/ec2/v2/home#Images:visibility=public-images;search=amzn-ami-hvm-2017.03.1.20170812-x86_64-gp2):
```bash
aws ec2 run-instances --image-id ami-657bd20a --count 1 --instance-type t2.medium --key-name <my-key-pair>
```
Now run the `compile.sh` script in `r/`.
You must pass the R version as a parameter to the script, e.g., `3.6.3`.
The script produces a zip containing a functional R installation in `/opt/R/`.
The relevant files can be found in `r/build/bin/`.
Use this R distribution for building the layers.

### Building custom layers (Don't use - Not updated)

In order to install additional R packages, you can create a lambda layer containing the libraries, just as in the second example. You must use the the compiled package files. The easiest way is to install the package with `install.packages()` and copy the resulting folder in `$R_LIBS`. Using only the package sources does not suffice. The file structure must be `R/library/<my-library>`. If your package requires system libraries, place them in `R/lib/`.

You can use Docker for building your layer. You need to run `./docker_build.sh` first. Then you can install your packages inside the container and copy the files to your machine. The `build.sh` script is used to run the docker container and copy sources to your machine. The `entrypoint.sh` script is used for installing packages inside the container.

We may need the following in our ~/serveRmore.yaml file for future Builder VMs:
```
aws:
  ssh_security_group:
  subnet:
builder:
  domain_name: null
  instance_id: null
  instance_type: t2.large
```
