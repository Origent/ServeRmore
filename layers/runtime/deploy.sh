#!/bin/bash

set -euo pipefail
NAME=$1
S3BUCKET=$2
S3KEY=$3

BASE_DIR=$(pwd)/runtime
BUILD_DIR=${BASE_DIR}/build
cd ${BUILD_DIR}/layer/
zip -r -q ${NAME}.zip .
mkdir -p ${BUILD_DIR}/dist/
mv ${NAME}.zip ${BUILD_DIR}/dist/
cd ${BUILD_DIR}/dist/
~/.local/bin/aws s3 cp ${BUILD_DIR}/dist/${NAME}.zip s3://${S3BUCKET}/${S3KEY}/${NAME}.zip 
~/.local/bin/aws lambda publish-layer-version \
    --layer-name ${NAME} \
    --content S3Bucket=${S3BUCKET},S3Key=${S3KEY}/${NAME}.zip
cd ${BASE_DIR}