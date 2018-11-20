# Contributing

Please reach out to Andrew Conklin for help getting started: aconklin@origent.com.

## Repackaging

```
python3 setup.py sdist
aws s3 cp dist/ServeRmore-0.0.1.tar.gz s3://origent-public-demo/survival-titanic/ServeRmore-0.0.1.tar.gz
```
