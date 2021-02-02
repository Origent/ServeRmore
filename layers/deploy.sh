#!/bin/bash

set -euo pipefail
VERSION=$1
S3BUCKET=$2
S3KEY=$3

BASE_DIR=$(pwd)
BUILD_DIR=${BASE_DIR}/build
cd ${BUILD_DIR}/layer/
zip -r -q r-runtime-${VERSION}.zip .
mkdir -p ${BUILD_DIR}/dist/
mv r-runtime-${VERSION}.zip ${BUILD_DIR}/dist/
cd ${BUILD_DIR}/dist/
version_="${VERSION//\./_}"
~/.local/bin/aws s3 cp ${BUILD_DIR}/dist/r-runtime-${VERSION}.zip s3://${S3BUCKET}/${S3KEY}/r-runtime-${VERSION}.zip 
~/.local/bin/aws lambda publish-layer-version \
    --layer-name r-runtime-${version_} \
    --content S3Bucket=${S3BUCKET},S3Key=${S3KEY}/r-runtime-${VERSION}.zip
cd ${BASE_DIR}