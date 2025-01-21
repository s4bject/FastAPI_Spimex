#!/bin/sh

echo "Waiting for Postgres to be ready..."
while ! pg_isready -h db -p 5432 > /dev/null 2>&1; do
  sleep 1
done

export PGPASSWORD=${POSTGRES_PASSWORD}

if psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c '\dt public.spimex_trading_results' | grep -q 'spimex_trading_results'; then
  echo "Table 'spimex_trading_results' already exists. Skipping restore."
else
  echo "Restoring database from dump..."
  if psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f /data/mydb.sql; then
    echo "Database restored successfully."
  else
    echo "Error restoring the database. Skipping..."
  fi
fi

exec uvicorn main:app --host 0.0.0.0 --port 8000
