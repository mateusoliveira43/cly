#!/bin/bash

ROOT="$(dirname $( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"
FILE="$ROOT/.env"
PROJECT='python-cli-script-template'

if ! test -f $FILE; then
    echo "USER_ID=$(id -u)" >> $FILE
    echo "GROUP_ID=$(id -g)" >> $FILE
    echo "PROJECT=$PROJECT" >> $FILE
    echo "WORK_DIR=/home/$PROJECT/$PROJECT" >> $FILE
    echo ".env file created in project's root"
fi
