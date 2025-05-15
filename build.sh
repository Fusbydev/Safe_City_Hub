#!/usr/bin/env bash

set -e  # stop if any command fails

echo "Installing dependencies..."
pip install -r requirements.txt

python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
