#!/bin/bash

set -euo pipefail

if [[ -z ${1+x} ]];
then
    echo 'version number required'
    exit 1
else
    VERSION=$1
fi

BASE_DIR=$(pwd)
BUILD_DIR=${BASE_DIR}/build/

cd ${BUILD_DIR}/layer/
zip -r -q r-runtime-${VERSION}.zip .
mkdir -p ${BUILD_DIR}/dist/
mv r-runtime-${VERSION}.zip ${BUILD_DIR}/dist/
version_="${VERSION//\./_}"
aws s3 cp ${BUILD_DIR}/dist/r-runtime-${VERSION}.zip s3://origent-api-dev/dx/als/r-runtime-${VERSION}.zip 
aws lambda publish-layer-version \
    --layer-name r-runtime-${version_} \
    --content S3Bucket=origent-api-dev,S3Key=dx/als/r-runtime-${VERSION}.zip
