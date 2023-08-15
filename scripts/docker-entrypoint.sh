#!/bin/sh
set -e
chmod +x docker-entrypoint.sh


# Check postgres service availability.
echo "Check postgres readiness"
python ~/check_service.py --service-name postgres --ip "${DATABASE_HOST-postgres}" --port "${DATABASE_PORT-5432}"

echo "Apply database migrations"
python manage.py migrate --noinput
