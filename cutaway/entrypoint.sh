#!/bin/sh

until pg_isready -h db -p 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 5
done

echo "Applying migrations..."
alembic revision --autogenerate -m "Migration"
alembic upgrade head
echo "Migrations applied."

exec "$@"