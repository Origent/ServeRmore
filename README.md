# ServeRmore

A package to improve fast and iterative workflow between RStudio and AWS Lambda Function hosting.  
Python Package Index Releases: https://pypi.org/project/serveRmore/

## Requirements

Please refer to our [LAPTOP.md Guide](https://github.com/Origent/ServeRmore/blob/master/LAPTOP.md) for necessary manual configurations.

To install the latest package:
```
python3 -m pip install serveRmore
```

## Quickstart

Please refer to your cloud platform for additional information:
* [AWS Lambda](AWS.md)
* [MS Azure Functions](AZURE.md)
* [Google Cloud Functions](GCP.md)

These commands are available for awareness.  
```
srm help
srm version
srm status
```

To deploy your R code directly to Lambda, try out our new workflow here.
```
srm lambda init
srm lambda create
srm lambda update
srm lambda invoke
srm lambda destroy
```

To create the packaging runtime environment and update the Handler function, package everything into a zip and store it, then deploy the zip to Serverless, run these commands:
```
srm create
srm update
srm package
srm deploy
srm terminate
```

## Roadmap

* Introduce new commands that allow using existing community Lambda layers for R without using a Python virtual environment.  Leverage an R Runtime and R Recommended layers.

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
