#!/bin/bash
set -e
# Start PostgreSQL check_service.py
echo "Check postgres readiness"
python /app/scripts/check_service.py --service-name postgres --ip "${DATABASE_HOST-postgres}" --port "${DATABASE_PORT-5432}"

# Apply database migrations (if needed)
echo "Apply database migrations"
python manage.py migrate --noinput

# Start Django development server
python manage.py runserver 0.0.0.0:8000

exec "$@"
