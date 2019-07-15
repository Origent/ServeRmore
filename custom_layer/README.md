## Custom R Runtime Layers

### Dependencies

* Install Docker Desktop on Mac or use an EC2 VM with the docker service installed.

### HowTo

1. Clone bakdata's 'aws-lambda-r-runtime' repo onto your machine.
```
git clone git@github.com:bakdata/aws-lambda-r-runtime.git
```

2. Copy the 'awspack' folder into a brand new layer folder and give it a descriptive name.
```
cd aws-lambda-r-runtime
cp -R awspack/ custom/
```

3. Open 'build.sh' and add copy the 'cd' and './build.sh' lines related to 'awspack', and paste into new lines.  Rename to match your new layer.

4. Go into your new custom folder, open up each file and ensure you rename "awspack" to your new layer name.

5. Change all 'package.install' values to match the new packages you want included in your custom runtime layer.

6. Go back to the root folder of the repo, and run './build.sh'.

7. After all the docker containers are pulled and code finishes executing, you should be able to publish your new Lambda Layer inside your AWS account by going into your custom folder and running './deploy.sh'
