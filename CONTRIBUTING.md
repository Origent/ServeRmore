# Contributing

Please reach out to Andrew Conklin for help getting started: https://github.com/adconk

Use the following command to rebuild the package and reinstall it locally for development and unit testing.  Verify the "VERSION.py" file is set the latest new version number that WILL BE published.  
```
python3 package.py
```

## Releasing

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

tbd
