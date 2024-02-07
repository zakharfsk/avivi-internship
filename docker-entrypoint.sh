#!/bin/bash

echo "Migrate..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Create superuser..."
python manage.py createsuperuser --noinput
