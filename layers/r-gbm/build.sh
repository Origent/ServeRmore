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

rm -rf ${BUILD_DIR}

mkdir -p ${BUILD_DIR}/layer/
docker run -v ${BUILD_DIR}/layer/:/var/r-gbm lambda-r:build-${VERSION}
sudo chown -R $(whoami):$(whoami) ${BUILD_DIR}/layer/
chmod -R 755 ${BUILD_DIR}/layer/
