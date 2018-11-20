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

After any manual cloud setup steps, you can then run the following commands.

To create the packaging runtime environment and update the Handler function, package and storage, then deploy to Serverless, run these commands:
```
srm create
srm update
srm package
srm deploy
srm terminate
```

Additionally, these commands are available for additional insight.
```
srm help
srm version
srm status
```

## Roadmap

We are closing in on our 1st package release, v0.0.1. Our objective is to be able to provide fast iteration on R ML modeling to API endpoint. In a future version, we'll add the ability to automate the creation and configuration of the initial runtime architecture.

To Do:
* Create a generic handler.py
* Practice updating RStudio code and redeploying to a Lambda Function

# Contributing

Please reach out to Andrew Conklin for help getting started: aconklin@origent.com. [CONTRIBUTING.md](CONTRIBUTING.md)
