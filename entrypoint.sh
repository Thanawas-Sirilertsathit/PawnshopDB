#!/bin/sh

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django development server
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000

# Build Tailwind CSS
echo "Building Tailwind CSS..."
python manage.py tailwind build
