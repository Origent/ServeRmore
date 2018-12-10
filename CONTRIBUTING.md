# Contributing

Please reach out to Andrew Conklin for help getting started: aconklin@origent.com.

## Repackaging

Please be sure to create a PyPi.org account and request access to deploy a package to our index repository.

Install the deploy dependency:
```
pip3 install --user --upgrade twine
```

Build your package and upload it to PyPi:
```
python3 setup.py sdist bdist_wheel
twine upload dist/*
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
