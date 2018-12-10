# ServeRmore

A package to improve fast and iterative workflow between RStudio and AWS Lambda Function hosting.

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

To create the packaging runtime environment and update the Handler function, package everything into a zip and store it, then deploy the zip to Serverless, run these commands:
```
srm create
srm update
srm package
srm deploy
srm terminate
```

## Roadmap

Our objective is to be able to provide fast iteration on R ML modeling to an API endpoint on AWS Lambda. In our next version, we plan to automate the creation of the handler.py file that is needed to start the instance of Lambda and provide the translation layer from HTTPS request, to Python Request, to R Request, and back again.

To Do:
* Create a generic handler.py
* Practice updating RStudio code and redeploying to a Lambda Function

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
