#!/usr/bin/env sh
set -e

# Espera o Postgres ficar pronto
until pg_isready -h "${DB_HOST:-psql}" -p "${DB_PORT:-5432}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null 2>&1; do
  echo "⏳ Aguardando Postgres em ${DB_HOST:-psql}:${DB_PORT:-5432}..."
  sleep 1
done
echo "✅ Postgres pronto!"

# Migrações + runserver
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
