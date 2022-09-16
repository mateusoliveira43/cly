#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
FILE="$ROOT/.env"
FILE="$ROOT/.env"
USER_NAME='develop'
SERVICE_NAME='cly'

if ! test -f $FILE; then
    echo "USER_ID=$(id -u)" >> $FILE
    echo "GROUP_ID=$(id -g)" >> $FILE
    echo "USER_NAME=$USER_NAME" >> $FILE
    echo "SERVICE_NAME=$SERVICE_NAME" >> $FILE
    echo "WORK_DIR=/home/$USER_NAME/$SERVICE_NAME" >> $FILE
    echo ".env file created in project's root"
fi
