#!/bin/bash

echo "Migrate..."
python manage.py migrate --noinput &&

echo "Collect static files..."
python manage.py collectstatic --noinput &&

echo "Create superuser..."
python manage.py createsuperuser --noinput &&

echo "Starting Gunicorn..."
extra_files=$(find /app/templates -name "*.html" -exec printf -- "--reload-extra-file {} " \;)
gunicorn 'config.wsgi' --bind=0.0.0.0:8000 --reload --reload-engine=poll $extra_files
