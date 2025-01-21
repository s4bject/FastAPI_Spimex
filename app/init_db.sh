#!/bin/sh

echo "Waiting for Postgres to be ready..."
until pg_isready -h db -p 5432; do
  sleep 1
done

export PGPASSWORD=${DB_PASS}

echo "Checking if the table already exists..."
if psql -h db -U ${DB_USER} -d ${DB_NAME} -c '\dt public.spimex_trading_results' | grep -q 'spimex_trading_results'; then
  echo "Table 'spimex_trading_results' already exists. Skipping restore."
else
  echo "Restoring database from dump..."
  psql -h db -U ${DB_USER} -d ${DB_NAME} -f /data/mydb.sql

  if [ $? -eq 0 ]; then
    echo "Database restored successfully."
  else
    echo "Error restoring the database. Continuing with the app..."
  fi
fi

echo "Starting the app..."
uvicorn main:app --host 0.0.0.0 --port 8000
