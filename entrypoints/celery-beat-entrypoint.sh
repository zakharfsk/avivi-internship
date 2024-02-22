#!/bin/bash

echo "Starting Celery Beat..."
celery -A config worker -B -E
