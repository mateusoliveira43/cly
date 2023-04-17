#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
$ROOT/docker/env.sh
. $ROOT/docker/base.sh

$DOCKER_COMPOSE \
--file $ROOT/docker/docker-compose.yaml \
--project-directory $ROOT \
run --rm cly $@
