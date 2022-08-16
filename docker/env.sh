#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
FILE="$ROOT/.env"
FILE="$ROOT/.env"
USER_NAME='develop'
PROJECT_NAME='python-cli-script-template'

if ! test -f $FILE; then
    echo "USER_ID=$(id -u)" >> $FILE
    echo "GROUP_ID=$(id -g)" >> $FILE
    echo "USER_NAME=$USER_NAME" >> $FILE
    echo "PROJECT_NAME=$PROJECT_NAME" >> $FILE
    echo "WORK_DIR=/home/$USER_NAME/$PROJECT_NAME" >> $FILE
    echo ".env file created in project's root"
fi
