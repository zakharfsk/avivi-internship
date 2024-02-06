#!/bin/sh

echo "Migrate..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Create superuser..."
python manage.py createsuperuser --noinput

start_gunicorn() {
    # Generate the reload-extra-file options dynamically
    extra_files=$(find /app/templates -name "*.html" -exec printf -- "--reload-extra-file {} " \;)

    # Start Gunicorn
    echo "Starting Gunicorn..."
    gunicorn 'config.wsgi' --bind=0.0.0.0:8000 --reload --reload-engine=poll $extra_files
}

start_gunicorn