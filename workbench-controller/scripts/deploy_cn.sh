#!/bin/bash

export AWS_PROFILE=default
export AWS_ACCOUNT=$(aws sts get-caller-identity | jq -r '.Account')
export AWS_DEFAULT_REGION=cn-northwest-1

TAG=latest

if [[ "$1" == "PROD" ]]; then
    HOST=52.83.206.28
    TAG=latest
else
    HOST=52.83.206.28
fi

REPO=${AWS_ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com.cn/workbench-controller:${TAG}

ssh -tt ubuntu@$HOST << EOF
    cd /opt/workbench-controller
    export $(grep -v '#.*' .env | xargs)

    set -ex
    $(aws ecr get-login --no-include-email)
    sudo docker pull ${REPO}
    (sudo docker rm -f workbench-controller || true)
    sudo docker run -d --restart always --name workbench-controller \
        -p 8999:8999 \
        -v $(pwd)/traefik-config:/app/traefik-config \
        ${REPO}
EOF

export $(cat .env | xargs)
docker run --name workbench-controller -d -p 8999:8999 -v $(pwd)/traefik-config:/app/traefik-config -v $(pwd)/.env:/app/.env ${REPO}

docker run -d -p 80:80 -v $(pwd)/traefik.yml:/etc/traefik/traefik.yml -v /var/run/docker.sock:/var/run/docker.sock traefik