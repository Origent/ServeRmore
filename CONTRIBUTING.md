# Contributing

Please reach out to Andrew Conklin for help getting started: aconklin@origent.com.

## Repackaging

```
python3 setup.py sdist
aws s3 cp dist/ServeRmore-0.0.1.tar.gz s3://origent-public-demo/survival-titanic/ServeRmore-0.0.1.tar.gz
```
## Debugging

If you're looking to add R packages inside the Lambda Runtime, you may have to add additional low level operating system libs. You can explore this after you have a working R Package, by doing the following:

1. Create a new SRM VM.
2. Run the following commands:

```
virtualenv ~/env && source ~/env/bin/activate
ldd /usr/lib64/R/bin/exec/R
```

This will tell you the required libs to run R.  It does not indicate whats required of additional packages, but this should give you a start.
