To run R through a Python 2.7 runtime on Lambda, you can invoke our deprecated workflow.  You will need a "handler.py" starter file, in addition a custom R package with the R code you want invoked in your function.

1. Develop an R package containing method interface calls and R package dependencies.

2. Ask us for a sample handler.py file that shows how to call your R package methods through Python with the r2py library.

3. Our entire workflow can be executed with the following commands:
```
srm create
srm update
srm package
srm deploy
srm terminate
```

NOTE: 'create' will create a brand new EC2 Virtual Machine and install CRAN and custom R packages depending on your config yaml settings.  'update' will reupload your handler.py file.  'package' will zip everything up and place on your S3 bucket and S3 bucket key.  'deploy' will publish your zip to your existing lambda function.
