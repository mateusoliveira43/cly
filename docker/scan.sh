#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"

docker build --tag python-cli-script-template --file $ROOT/docker/Dockerfile .
docker login
docker scan --exclude-base --file $ROOT/docker/Dockerfile python-cli-script-template
docker logout
