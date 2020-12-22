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
./docker_build.sh ${VERSION}
cd ${BASE_DIR}/r
./build.sh ${VERSION}
cd ${BASE_DIR}/r-runtime
./build.sh
cd ${BASE_DIR}/r-gbm
./build.sh ${VERSION}
