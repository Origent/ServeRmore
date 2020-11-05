#!/bin/bash

set -euo pipefail

if [[ -z ${1+x} ]];
then
    echo 'version number required'
    exit 1
else
    VERSION=$1
fi

if [[ -z ${2+x} ]];
then
    echo 'bucket name required'
    exit 1
else
    BUCKET=$2
fi

if [[ -z ${3+x} ]];
then
    echo 'instance profile required'
    exit 1
else
    PROFILE=$3
fi

instance_id=$(aws ec2 run-instances --image-id ami-02507631a9f7bc956 --count 1 --instance-type t2.medium \
    --instance-initiated-shutdown-behavior terminate --iam-instance-profile Name='"'${PROFILE}'"' \
    --user-data '#!/bin/bash
chmod u+rwx r/compile.sh r/build.sh r-runtime/build.sh r-gbm/build.sh build.sh r-runtime/deploy.sh r-gbm/deploy.sh
yum install -y git
git clone https://github.com/Origent/ServeRmore.git
cd ServeRmore/
./r/compile.sh '"$VERSION"'
./build.sh '"$VERSION"'
./r-runtime/deploy.sh '"$VERSION"'
./r-gbm/deploy.sh '"$VERSION"'
shutdown -h now' \
    --query 'Instances[0].InstanceId' --output text)

until aws ec2 wait instance-terminated --instance-ids ${instance_id} 2>/dev/null
do
    echo "Still waiting for $instance_id to terminate"
    sleep 10
done
