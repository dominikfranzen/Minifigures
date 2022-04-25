#!/bin/bash
#You need to be logged in to dockerhub
docker buildx create --name m1builder
docker buildx use m1builder
docker buildx build --tag unbrickable-webapp:latest -o type=image --platform=linux/arm64,linux/amd64 .
docker buildx build --push --tag dominikfranzen/unbrickable-webapp:latest --platform=linux/arm64,linux/amd64 .