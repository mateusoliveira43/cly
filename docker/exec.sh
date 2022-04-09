#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
$ROOT/docker/env.sh

while read line; do
    if [[ "$line" == *'PROJECT='* ]]; then
        PROJECT=${line#*=}
    fi
done < $ROOT/.env

docker-compose \
--file $ROOT/docker/docker-compose.yaml \
--project-directory $ROOT \
up --detach

docker-compose \
--file $ROOT/docker/docker-compose.yaml \
--project-directory $ROOT \
exec $PROJECT sh
