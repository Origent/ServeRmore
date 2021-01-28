## Custom R Runtime Layers

To build and publish your own R base runtime layer with your selected R packages, make sure the following is set in your '~/serveRmore.yaml' file in the instance you're planning to run "srm build" from:

### Dependencies

* srm cli is installed from Python Package Index as mentioned in the main [README](../README.md).
* We rely on the Docker agent pre-installed on Amazon Linux 2 in the Amazon Machine Image ID provided in the sample yaml file snippet above.
* We have used the following repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime

### HowTo

1. In addition to the utility, we'll need to clone/copy the repo as well:
```
git clone git@github.com:Origent/ServeRmore.git
```

2. Double check your ~/serveRmore.yaml to make sure it's configured for creating a new Lambda layer.  In additon to to what was recommended from the main [README][../README.md], we want to double check several other fields. We create a temporary EC2 virtual machine with Docker, so that we can build our runtime layer.  When we create a new EC2 instance, we want to make sure they are all in the same default security group.  Also, we want to select a subnet address to use. The ssh security group is a group we create ourselves so that we can allow SSH port 22.

NOTE: both 'domain_name' and 'instance_id' should be left blank as those are updated automatically.

Now, if all is setup correctly, we did the heavy lifting.  Building and Publishing the new R runtime layer only requires us to run three commands and wait for them to complete.  
```
srm create
srm deploy
srm terminate
```

NOTE: Only R v4.0.2 is tested and supported at this time.

3. In the "srm deploy" command, we are running another build script behind the scenes for the R base compilation and R runtime layer setup with optional additional packages. The build and compilation process uses a Docker image called [docker-lambda](https://github.com/lambci/docker-lambda).

4. Double check the AWS Lambda Console and Layers registry as well as your serveRmore.yaml file to confirm that your layer was indeed published.

### Debugging

If there are challenges with the layer build, the following can be run to interact with the environment inside the docker service used to build the layer. Once inside the Terminal of the Docker container, the individual commands listed in Dockerfile can be run. Before running, make sure you have already run build.sh at least once:
```
docker run -it lambda-r:build-4.0.2 bash
```

If you're curious what shared libraries outside of the installed R folder is being used in the build environment, you can run the following to get a list:
```
ldd /usr/lib64/R/bin/exec/R
```

Additional log entries from the runtime layer can be placed in the Lambda Service by adding print commands to the following file and function.  Also, example print statements are provided:

FILENAME: ServeRmore/layer/r-runtime/build/layers/r-runtime/build/layer/R/library/base/R/Rprofile
METHOD: .First.sys()
```
print(paste0("PATH = ", Sys.getenv("PATH")))
print(paste0("Listing files in PATH /usr/local/bin:", paste(list.files("/usr/local/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /usr/bin/:", paste(list.files("/usr/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /bin:", paste(list.files("/bin/"), collapse = ",")))
print(paste0("Listing files in PATH /opt/bin", paste(list.files("/opt/bin/"), collapse = ",")))
print(paste0("R.home() = ", file.path(R.home())))
print(paste0("Listing files in ", file.path(R.home(), "library"), ":", paste(list.files(file.path(R.home(), "library")), collapse = ",")))
```

It is possible to test the 'current' directory where the runtime layer build exists in an unzipped capacity in the VM, with a super basic handler.R script that can contain something as simple as 'print("Hello World!")'. The following command maps the current directory into the Docker container service and the expected execution folder, and runs the local handler.R file against the runtime.  This is not fully developed and is only theoretical for us right now:
```
docker run --rm -v "$PWD":/opt:ro,delegated lambda-r:build-4.0.2 handler.R
```

### r-runtime layer

We recommend that the r-runtime base layer has the following packages installed.  If you remove any of these, you'll run the risk of not having a working R runtime layer.

R,
[httr](https://cran.r-project.org/package=httr),
[jsonlite](https://cran.r-project.org/package=jsonlite),
[aws.s3](https://cran.r-project.org/package=aws.s3),
[logging](https://cran.r-project.org/package=logging),
[yaml](https://cran.r-project.org/package=yaml)

## Limitations

AWS Lambda is limited to running with 3GB RAM and must finish within 15 minutes. It is therefore not feasible to execute long running R scripts with this runtime. Furthermore, only the `/tmp/` directory is writeable on AWS Lambda. This must be considered when writing to the local disk.

## Creating your own Layer

If you decide to create your own layer, here's a few things to think about and a few steps to help you get started.

Concepting:
  1. Keep in mind the limits in how many layers a Lambda Function can have. I believe this remains a modest number.
  2. Keep in mind the Lambda Layer zip package size limits.  It is extremely unlikely to be able to package up the entire Tidyverse as a layer, for example.  This could change as the AWS Lambda Service changes its requirements.  
  3. Keep in mind, the more you add, the slower the Function performance will be come, as you'll be spending a lot more time starting up the environment to run the function code.  
  4. Precision is important.  Unlike an R&D or exploratory programming environment, each decision has an impact on functionality, performance, and quality.
  
In a future release, we're considering expanding out beyond 1 layer only. Stay tuned.
