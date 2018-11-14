# ServeRmore

A package to improve fast and iterative workflow between RStudio and AWS Lambda Function hosting.

## Prerequisites

Please refer to our [LAPTOP.md Guide](LAPTOP.md) for necessary manual configurations.

## Developing

```
python3 setup.py sdist
aws s3 cp dist/ServeRmore-0.0.1.tar.gz s3://origent-public-demo/survival-titanic/ServeRmore-0.0.1.tar.gz
aws s3 cp s3://origent-public-demo/survival-titanic/ServeRmore-0.0.1.tar.gz ServeRmore-0.0.1.tar.gz
pip3 install ServeRmore-0.0.1.tar.gz
```

We are closing in on our 1st package release, v0.0.1. Our objective is to be able to provide fast iteration on R ML modeling to API endpoint. In a future version, we'll add the ability to automate the creation and configuration of the initial runtime architecture.

To Do:
* Create a generic handler.py
* Practice updating RStudio code and redeploying to a Lambda Function
* Setup a Test API and practice with it

# Contributing

Please reach out to Andrew Conklin for help getting started: aconklin@origent.com.
