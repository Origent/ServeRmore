# AWS Configuration

## Prerequisites

Before this utility can be used, there are a number of assumptions made about your AWS environment.  

If you have a master account or your IAM account is provided full admin permissions, you can skip over the permissions section.

Permissions:
  * Can create and terminate EC2 instances
  * Can create API Gateways & Modify them
  * Can create Lambda Functions & Modify them
  * Can create S3 Buckets & Modify them

Architecture:
  * Create your API Gateway through the AWS console
  * Create a Lambda Function through the AWS console
  * Connect your Function to your API.


## Steps

It is recommended that you run a single informational srm command before proceeding with the quickstart, that way you can modify your configuration file with AWS specific settings.

1. Run the following:

```
srm help
```

2. Open ~/serveRmore.yaml file in your text editor.  These values will need to be filled out. 
