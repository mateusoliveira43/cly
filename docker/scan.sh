#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"

docker build --tag cly - < $ROOT/docker/Dockerfile
docker login
# docker scan --login --token <TOKEN>
# rm -rf  ~/.config/configstore/snyk.json
docker scan --severity medium --file $ROOT/docker/Dockerfile cly
docker logout
