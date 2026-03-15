#!/bin/bash
set -e

# Wait for DB to be ready (optional, avoids connection refused)
echo "Waiting for PostgreSQL..."
sleep 5

# Create tables
python run.py --create-tables

# Start Gunicorn
exec gunicorn run:app --bind 0.0.0.0:10000