## Roadmap

v0.1.1 - Additional Updates
* Add multi-layer support
* Remove the dependency of cloning the repo locally along with installing the utility to build layers

## Changelog

v0.1.0 - Revamped Lambda Service Layers and removed outdated deployment steps

* Added support for R v4.0.2 
* Simplified the layer building process and scripts
* Support for one custom runtime layer for R with customizable R packages
* Auto-Save of the ARN for new runtime layer 
* Removed reliance on r2py, Python 2, and R 3.4.2

v0.0.2 - Introduces running R directly on Lambda via new AWS custom layers feature, big thanks to [@bakdata](https://github.com/bakdata).

* Several new commands for initiating the R runtime version, creating new functions, updating them, and destroying them.
* New documentation for how to build a custom R layer.

v0.0.1 - Initial Release

* Automated a genomics analysis guide that used Lambda with R.  Introduces an automated build process that creates a temporary AWS EC2 Virtual Machine, installs an R environment with CRAN and custom R packages, wraps them into a Lambda Package.  Also requires manual development of a Handler.py file that calls the R environment and R methods through r2py.
* Provides an easy way to iterate and repackage after handler.py changes.
