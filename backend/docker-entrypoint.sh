#!/bin/sh
set -e

echo "Waiting for database..."
python scripts/wait_for_db.py

echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"
