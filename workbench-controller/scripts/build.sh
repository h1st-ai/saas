#!/bin/bash

set -e
TAG=${1:-"latest"}

REPO=394497726199.dkr.ecr.us-west-1.amazonaws.com
docker build . -t h1st/workbench-controller:$TAG

if [[ "$PUSH" == "yes" ]]; then
    aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin $REPO
    docker tag h1st/workbench-controller:$TAG $REPO/h1st/workbench-controller:$TAG
    docker push $REPO/h1st/workbench-controller:$TAG
else
    echo "Set PUSH=yes to push to ECR"
fi
