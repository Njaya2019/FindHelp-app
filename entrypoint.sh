#!/bin/bash
set -e

DATA_DIR="/home/postgresuser/data"
mkdir -p "$DATA_DIR"

PG_BIN=$(find /usr/lib/postgresql -name "initdb" -type f -exec dirname {} \; | sort | tail -n 1)

if [ ! -f "$DATA_DIR/PG_VERSION" ]; then
    echo "Initializing Postgres..."
    "$PG_BIN/initdb" -D "$DATA_DIR" -A trust
fi

echo "Starting Postgres..."

"$PG_BIN/postgres" -D "$DATA_DIR" -p 5432 -k /tmp > "$DATA_DIR/postgres.log" 2>&1 &
PG_PID=$!

sleep 5

echo "------ POSTGRES LOG ------"
cat "$DATA_DIR/postgres.log"
echo "--------------------------"

"$PG_BIN/pg_isready" -h localhost -p 5432

# Wait a few seconds for Postgres to be ready
sleep 5

# Create tables
python run.py --create-tables

# Start Flask via Gunicorn
exec gunicorn run:app --bind 0.0.0.0:10000
# exec python -m gunicorn run:app --bind 0.0.0.0:10000

# Cleanup: stop Postgres if container stops
trap "kill $PG_PID" EXIT