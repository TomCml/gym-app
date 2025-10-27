#!/bin/bash
set -e

echo "--- Checking commands ---"
which nc
which alembic
which psql
which python
which uvicorn
echo "--- End Checks ---"

# Wait for PostgreSQL
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Running database migrations..."
alembic upgrade head || echo "Migration failed, continuing..."

# Seed database
echo "Checking if database needs seeding..."
EXERCISE_COUNT=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -tAc "SELECT COUNT(*) FROM exercises;" 2>/dev/null || echo "0")

if [ "$EXERCISE_COUNT" = "0" ]; then
    echo "Database is empty. Populating with seed data..."
    PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /backend/seed_exercises.sql
    echo "Database populated successfully."
else
    echo "Database already contains $EXERCISE_COUNT exercises. Skipping population."
fi

# Start the application
echo "Starting FastAPI app..."
exec "$@"