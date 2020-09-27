#!/bin/bash

REPO=394497726199.dkr.ecr.us-west-1.amazonaws.com
TAG=latest

CLUSTER=${1:-"dev"}

if [[ "$1" == "PROD" ]]; then
    HOST=10.30.0.142
    TAG=${2:-"0.2.0"}
else
    HOST=10.30.128.207
fi

ssh ubuntu@$HOST << EOF
    cd /opt/workbench-controller
    export \$(grep -v '#.*' .env | xargs)

    set -ex
    aws ecr get-login-password --region us-west-1 | sudo docker login --username AWS --password-stdin $REPO
    sudo docker pull $REPO/h1st/workbench-controller:$TAG
    (sudo docker rm -f workbench-controller || true)
    sudo docker run -d --restart always --name workbench-controller \
        -p 8999:8999 \
        -v \`pwd\`/traefik-config:/app/traefik-config \
        -v \`pwd\`/.env:/app/.env \
        $REPO/h1st/workbench-controller:$TAG
EOF
