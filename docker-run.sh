#!/usr/bin/env bash

VENV_PYTHON="../venv/bin/python"

MANAGE="$VENV_PYTHON manage.py"

if [ -z $1 ] || [ $1 = 'run' ]; then
    $MANAGE migrate
    $MANAGE runserver 0.0.0.0:9000
elif [ $1 = 'dumpdata' ]; then
    $MANAGE dumpdata
else
    echo "unknown command / parameters $@"
    exit 1
fi
