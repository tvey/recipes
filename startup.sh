#!/bin/sh

#restart this script as root, if not already root
[ `whoami` = root ] || exec sudo $0 $*

pipenv install --skip-lock --system --dev

python manage.py runserver 0.0.0.0:8000