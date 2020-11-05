## Custom R Runtime Layers

### Dependencies

* Install Docker Desktop on Mac or use an EC2 VM with the docker service installed.
* We have used the following repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime

### HowTo

You can build two layers from scratch.  Please take the following steps to complete.

1. We want to make sure that shell/terminal scripts are executable.
```
cd ServeRmore/layers
chmod u+rwx -R *.sh
chmod u+rwx -R r/*.sh
chmod u+rwx -R r-runtime/*.sh
chmod u+rwx -R r-gbm/*.sh
```

2. Double check several scripts to ensure they are correct for R v4.x or a newer version you might be working with.  Namely, the Dockerfile "ARG VERSION=x.x.x" variable and the r/compile.sh script with the wget line.  the URL in the wget line specifies R-3, for 3.x.x versions of base R, but should say R-4 for 4.x.x versions of base R.

3. We will run the build script for the R base, R layer, and GBM layer. To build the layers yourself, you need to first build R from source. We provide a Docker image which uses the great [docker-lambda](https://github.com/lambci/docker-lambda) project. You can build R, R runtime layer, and R gbm layer all at once.  Just do the following with your version number and everything should be build properly.
```
./build.sh 4.0.2
```

4. We then run the deploy script for the R layer and GBM layer. This publishes to your AWS account if you have previously followed the LAPTOP setup guide and you have an active AWS account.

If you plan to publish the runtime and gbm layers, you need to have a recent version of aws cli (>=1.16). When you run the deploy script with your version number, it creates two lambda layers named `r-<layer>-<version>` in your AWS account.
```
./deploy.sh 4.0.2
```

### r-runtime

The r-runtime base layer has the following packages installed.

R,
[httr](https://cran.r-project.org/package=httr),
[jsonlite](https://cran.r-project.org/package=jsonlite),
[aws.s3](https://cran.r-project.org/package=aws.s3),
[logging](https://cran.r-project.org/package=logging),
[yaml](https://cran.r-project.org/package=yaml)

### r-gbm

The r-gbm base layer has the following packages installed.

[Matrix](https://cran.r-project.org/package=Matrix),
[survival](https://cran.r-project.org/package=survival)
[gridExtra](https://cran.r-project.org/package=gridExtra)
[lattice](https://cran.r-project.org/package=lattice)
[gbm](https://cran.r-project.org/package=gbm)

### Debugging

In order to make the runtime log debugging messages, you can set the environment variable `LOGLEVEL` to `DEBUG`.

## Limitations

AWS Lambda is limited to running with 3GB RAM and must finish within 15 minutes. It is therefore not feasible to execute long running R scripts with this runtime. Furthermore, only the `/tmp/` directory is writeable on AWS Lambda. This must be considered when writing to the local disk.

### Compiling on EC2 (TBD)

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

### Building custom layers (TBD)

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
