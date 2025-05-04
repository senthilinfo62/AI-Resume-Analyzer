#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
max_retries=30
counter=0
while ! python -c "import MySQLdb; MySQLdb.connect(host='db', user='root', passwd='admin@123', db='resume_analyzer')" 2>/dev/null; do
    counter=$((counter+1))
    if [ $counter -gt $max_retries ]; then
        echo "Failed to connect to database after $max_retries attempts. Exiting."
        exit 1
    fi
    echo "Database not ready yet. Waiting... ($counter/$max_retries)"
    sleep 2
done
echo "Database is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created.')
else:
    print('Superuser already exists.')
"

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
