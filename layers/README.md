## Custom R Runtime Layers

To build and publish new layers for base R and R GBM, make sure the following is set in your '~x/serveRmore.yaml' file in the instance you're planning to run "srm create" from:
```
layers:
  ssh_security_group: null
  subnet: null
  instance_type: t2.large
  domain_name: null
  instance_id: null
  private_key: null
```

### Dependencies

* Install Docker Desktop on Mac or use an EC2 VM with the docker service installed.
* We have used the following repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime

### HowTo

You can build two layers from scratch.  Please take the following steps to complete.

1. Use the "srm" utility to create a new VM.  Then login to it.  The ServeRmore repo should already be in your home folder.
```
srm create
srm ssh
cd ServeRmore/layers
```

2. We will run the build script for the R base, R layer, and GBM layer. To build the layers yourself, you need to first build R from source. We provide a Docker image which uses the great [docker-lambda](https://github.com/lambci/docker-lambda) project. You can build R, R runtime layer, and R gbm layer all at once.  Just do the following with your version number and everything should be build properly.
```
./build.sh 4.0.2
```

6. We then run the deploy script for the R layer and GBM layer. This publishes to your AWS account if you have previously followed the LAPTOP setup guide and you have an active AWS account. If you plan to publish the runtime and gbm layers, you need to have a recent version of aws cli (>=1.16). When you run the deploy script with your version number, it creates two lambda layers named `r-<layer>-<version>` in your AWS account.
```
./deploy.sh 4.0.2
```

### Debugging

If there are challenges with the layer build, the following can be run to interact with the environment inside the docker service used to build the layer. Once inside the Terminal of the Docker container, the individual commands listed in Dockerfile can be run. Before running, make sure you have already run build.sh at least once:
```
docker run -it lambda-r:build-4.0.2 bash
```

If you're curious what shared libraries outside of the installed R folder is being used in the build environment, you can run the following to get a list:
```
ldd /usr/lib64/R/bin/exec/R
```

It is possible to test the 'current' directory where the runtime layer build exists in an unzipped capacity in the VM, with a super basic handler.R script that can contain something as simple as 'print("Hello World!")'. The following command maps the current directory into the Docker container service and the expected execution folder, and runs the local handler.R file against the runtime.  This is not fully developed and is only theoretical for us right now:
```
docker run --rm -v "$PWD":/opt:ro,delegated lambda-r:build-4.0.2 handler.R
```

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
