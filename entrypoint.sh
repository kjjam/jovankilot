#!/bin/bash

python manage.py makemigrations installation
python manage.py migrate
python manage.py collectstatic

gunicorn --bind 0.0.0.0:8000 javan_locksmith.asgi -w 4 -k uvicorn.workers.UvicornWorker