#!/bin/bash

echo "Starting Celery..."
celery -A config worker -l info -E
