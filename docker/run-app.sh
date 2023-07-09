#!/usr/bin/env bash

VENV_BIN="./venv/bin/"

MANAGE="${VENV_BIN}/django-admin"

if [ -z $1 ] || [ $1 = 'run' ]; then
    $MANAGE migrate
    $MANAGE runserver 0.0.0.0:9000
elif [ $1 = 'dumpdata' ]; then
    $MANAGE dumpdata
elif [ $1 = 'shell' ]; then
    /bin/bash
else
    echo "unknown command / parameters $@"
    exit 1
fi
