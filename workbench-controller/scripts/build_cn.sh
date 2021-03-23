#!/bin/bash

#export AWS_PROFILE=cn
export AWS_ACCOUNT=$(aws sts get-caller-identity | jq -r '.Account')
export AWS_DEFAULT_REGION=cn-northwest-1

set -e
TAG=${1:-"latest"}

REPO=${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com.cn/workbench-controller:${TAG}
docker build . -t workbench-controller:$TAG

if [[ "$PUSH" == "yes" ]]; then
    $(aws ecr get-login --no-include-email)
    docker tag workbench-controller:$TAG ${REPO}
    docker push ${REPO}
else
    echo "Set PUSH=yes to push to ECR"
fi
