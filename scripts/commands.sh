#!/usr/bin/env sh
set -e

echo ">> Rodando migrations..."
python manage.py migrate --noinput

# Se quiser coletar estáticos (somente se usar arquivos estáticos):
# echo ">> Coletando arquivos estáticos..."
# python manage.py collectstatic --noinput

echo ">> Subindo Gunicorn..."
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info
