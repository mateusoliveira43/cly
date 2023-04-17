DOCKER_COMPOSE_BIN="docker-compose"
DOCKER_COMPOSE_FROM_DOCKER="docker compose"
DOCKER_COMPOSE=""

if [ -x "$(command -v $DOCKER_COMPOSE_BIN)" ]; then
  DOCKER_COMPOSE=$DOCKER_COMPOSE_BIN
elif [ -x "$(command -v $DOCKER_COMPOSE_FROM_DOCKER)" ]; then
  DOCKER_COMPOSE=$DOCKER_COMPOSE_FROM_DOCKER
else
  echo "Neither 'docker-compose' and 'docker compose' found. At least one of them are mandatory."
  exit 1
fi
