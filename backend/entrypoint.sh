#!/bin/sh

VENV_BIN="/opt/venv/bin"


echo "--- Checking commands ---"
which nc
which alembic 
which /usr/lib/postgresql/15/bin/psql    
which python  
which uvicorn 
echo "--- End Checks ---"



echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Running database migrations..."
$VENV_BIN/python -m alembic upgrade head 

echo "Checking if database needs seeding..."
EMPTY=$(/usr/lib/postgresql/15/bin/psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT EXISTS (SELECT 1 FROM exercises LIMIT 1);")
if [ "$(echo $EMPTY | xargs)" = "f" ]; then
  echo "Populating database..."
  /usr/lib/postgresql/15/bin/psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -f /home/appuser/backend/seed_exercises.sql  
else
  echo "Skipping population."
fi

echo "Starting FastAPI app..."
exec $VENV_BIN/python -m uvicorn main:app --host 0.0.0.0 --port 8000