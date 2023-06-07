#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py scrape
python manage.py collectstatic --no-input
gunicorn my_cv.wsgi:application --bind 0.0.0.0:8000
