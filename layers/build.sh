#!/bin/bash

set -euo pipefail
VERSION=$1
IFS=', ' read -r -a array <<< "$2"
PACKAGES=${array[@]}

BASE_DIR=$(pwd)
BUILD_DIR=${BASE_DIR}/build
mkdir -p ${BUILD_DIR}/bin/
mkdir -p ${BUILD_DIR}/layer/R/
docker build . -t lambda-r:build-${VERSION} --build-arg VERSION=${VERSION} --build-arg PACKAGES=${PACKAGES}
docker run -v ${BUILD_DIR}/bin/:/var/r lambda-r:build-${VERSION}
sudo chown -R $(whoami):$(whoami) ${BUILD_DIR}/bin/
cp ${BASE_DIR}/src/* ${BUILD_DIR}/layer/
cd ${BUILD_DIR}/layer/
cp -r ${BUILD_DIR}/bin/* R/
recommended=(boot class cluster codetools foreign KernSmooth MASS mgcv nlme nnet rpart spatial)
for package in "${recommended[@]}"
do
   rm -r R/library/${package}/
done
chmod -R 755 .
cd ${BASE_DIR}
