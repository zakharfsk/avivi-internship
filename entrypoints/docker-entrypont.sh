echo "Migrate..."
python manage.py migrate

echo "Collect static files..."
python manage.py collectstatic --noinput

echo "Create superuser..."
python manage.py createsuperuser --noinput

echo "Run server..."
gunicorn 'config.wsgi' --bind=0.0.0.0:8000 --reload