## Custom R Runtime Layers

### Dependencies

* We have used this repo for inspiration on managing our layers: https://github.com/bakdata/aws-lambda-r-runtime
* Install Docker Desktop on Mac or use an EC2 VM with the docker service installed.

You'll also need the following in your ~/serveRmore.yaml file:
```
aws:
  ssh_security_group:
  subnet:
builder:
  ami: ami-02507631a9f7bc956
  cran_r_package_names:
  - survival
  - gbm
  domain_name: null
  instance_id: null
  instance_type: t2.large
```

### HowTo

You can build the layer from scratch.  

1. Open the root 'build.sh' and copy the 'cd' and './build.sh' lines inside the file related to 'awspack', and paste into new lines.  Rename to match your new layer, 'origent'.

2. Go into your new custom 'origent' folder, open up each file and ensure you rename "awspack" to your new layer name. Change all 'package.install' values to match the new packages you want included in your new custom runtime layer.

3. Go back to the root folder of the repo, and run './build.sh'.

4. After all the docker containers are pulled and code finishes executing, you should be able to publish your new Lambda Layer inside your AWS account by going into your custom 'origent' folder and running './deploy.sh'

### r-runtime

R,
[httr](https://cran.r-project.org/package=httr),
[jsonlite](https://cran.r-project.org/package=jsonlite),
[aws.s3](https://cran.r-project.org/package=aws.s3),
[logging](https://cran.r-project.org/package=logging),
[yaml](https://cran.r-project.org/package=yaml)

## Other Documentation

The lambda handler is used to determine both the file name of the R script and the function to call.
The handler must be separated by `.`, e.g., `script.handler`.

The lambda payload is unwrapped as named arguments to the R function to call, e.g., `{"x":1}` is unwrapped to `handler(x=1)`.

The lambda function returns whatever is returned by the R function as a JSON object.

### Building custom layers

In order to install additional R packages, you can create a lambda layer containing the libraries, just as in the second example.
You must use the the compiled package files.
The easiest way is to install the package with `install.packages()` and copy the resulting folder in `$R_LIBS`.
Using only the package sources does not suffice.
The file structure must be `R/library/<my-library>`.
If your package requires system libraries, place them in `R/lib/`.

You can use Docker for building your layer.
You need to run `./docker_build.sh` first.
Then you can install your packages inside the container and copy the files to your machine.
See `awspack/` for an example.
The `build.sh` script is used to run the docker container and copy sources to your machine.
The `entrypoint.sh` script is used for installing packages inside the container.

### Debugging

In order to make the runtime log debugging messages, you can set the environment variable `LOGLEVEL` to `DEBUG`.

## Limitations

AWS Lambda is limited to running with 3GB RAM and must finish within 15 minutes.
It is therefore not feasible to execute long running R scripts with this runtime.
Furthermore, only the `/tmp/` directory is writeable on AWS Lambda.
This must be considered when writing to the local disk.


## Building

To build the layer yourself, you need to first build R from source.
We provide a Docker image which uses the great [docker-lambda](https://github.com/lambci/docker-lambda) project.
Just run `./build.sh <version>` and everything should be build properly.

If you plan to publish the runtime, you need to have a recent version of aws cli (>=1.16).
Now run the `<layer>/deploy.sh` script.
This creates a lambda layer named `r-<layer>-<version>` in your AWS account.
You can use it as shown in the example.

### Compiling on EC2

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
