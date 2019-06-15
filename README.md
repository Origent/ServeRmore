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

https://github.com/bakdata/aws-lambda-r-runtime
```
# example 'create' command code:
aws lambda create-function --function-name dx-hd-pred \
    --zip-file fileb://lambda.zip --handler matrix.handler \
    --runtime provided --timeout 60 --memory-size 3008 \
    --layers arn:aws:lambda:us-east-1:131329294410:layer:r-runtime-3.5.3 \
        arn:aws:lambda:us-east-1:131329294410:layer:r-recommended-3.5.3 \
    --role <role-arn> --region us-east-1

#Get latest layer version for runtime
aws lambda list-layer-versions --max-items 1 --no-paginate --layer-name arn:aws:lambda:us-east-1:131329294410:layer:r-runtime-3_5_3 --query 'LayerVersions[0].LayerVersionArn' --output text

#Get latest layer version for recommended
aws lambda list-layer-versions --max-items 1 --no-paginate --layer-name arn:aws:lambda:us-east-1:131329294410:layer:r-recommended-3_5_3 --query 'LayerVersions[0].LayerVersionArn' --output text
```


## Contributing

Please refer to our guide for more information. [CONTRIBUTING.md](CONTRIBUTING.md)
