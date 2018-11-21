# ServeRmore

A package to improve fast and iterative workflow between RStudio and AWS Lambda Function hosting.

## Requirements

Please refer to our [LAPTOP.md Guide](LAPTOP.md) for necessary manual configurations.

To install the latest package, run these two commands:
```
aws s3 cp s3://origent-public-demo/survival-titanic/ServeRmore-0.0.1.tar.gz ServeRmore-0.0.1.tar.gz

pip3 install ServeRmore-0.0.1.tar.gz
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

We are closing in on our 1st package release, v0.0.1. Our objective is to be able to provide fast iteration on R ML modeling to API endpoint. In a future version, we'll add the ability to automate the creation and configuration of the initial runtime architecture.

To Do:
* Create a generic handler.py
* Practice updating RStudio code and redeploying to a Lambda Function

## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
