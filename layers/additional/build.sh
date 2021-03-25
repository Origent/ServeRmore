#!/bin/bash

set -euo pipefail
VERSION=$1
PACKAGES=$2

BASE_DIR=$(pwd)/additional
BUILD_DIR=${BASE_DIR}/build
mkdir -p ${BUILD_DIR}/bin/
mkdir -p ${BUILD_DIR}/layer/R/library
docker build ./runtime -t lambda-r:build-${VERSION} --build-arg VERSION=${VERSION} --build-arg PACKAGES="${PACKAGES}"
docker run -v ${BUILD_DIR}/bin/:/var/r lambda-r:build-${VERSION}
sudo chown -R $(whoami):$(whoami) ${BUILD_DIR}/bin/
cd ${BUILD_DIR}/layer/R/library
for package in ${PACKAGES}
do
  cp -r ${BUILD_DIR}/bin/library/${package} ${package}
done
chmod -R 755 .
cd ${BASE_DIR}
