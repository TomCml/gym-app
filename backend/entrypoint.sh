#!/bin/bash
set -e

echo "--- Checking commands ---"
which nc
which alembic
which psql
which python
which uvicorn
echo "--- End Checks ---"

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

echo "Running database migrations..."
alembic upgrade head

echo "Seeding database..."
python /backend/seed.py

echo "Starting server..."
# Fixed: Use 'main:app' to match your flat structure; --reload for dev
uvicorn main:app --host 0.0.0.0 --port 8000 --reload