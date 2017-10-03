#!/bin/bash

set -eu

# Docker Hub User
DH_USER=takahasi

# Docker Hub Repository
DH_REPO=docker-openrtm-examples

# Docker Hub Image Tag
TAG=start-examples

# Build image
docker build --tag=$DH_USER/$DH_REPO:$TAG .
docker images

# Push built image
docker login
docker push $DH_USER/$DH_REPO:$TAG

exit 0
