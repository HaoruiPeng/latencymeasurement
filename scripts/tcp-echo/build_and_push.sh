#!/bin/zsh

docker login registry.gitlab.com

CURRENT_DIR="${PWD##*/}"
IMAGE_NAME="tcp-server"

REGISTRY="registry.gitlab.com/haorui/docker_images"
docker build -t ${REGISTRY}/${IMAGE_NAME}:latest -t ${REGISTRY}/${IMAGE_NAME}:latest -f Dockerfile .
docker push ${REGISTRY}/${IMAGE_NAME}:latest
