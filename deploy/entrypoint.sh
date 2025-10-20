#!/usr/bin/env bash
set -e

# Ждём базу данных (PostgreSQL)
if [ -n "$DATABASE_HOST" ]; then
  echo "⏳ Waiting for database at $DATABASE_HOST:$DATABASE_PORT..."
  until nc -z $DATABASE_HOST $DATABASE_PORT; do
    sleep 1
  done
fi

# Применяем миграции и собираем статику
python manage.py migrate --noinput
python manage.py collectstatic --noinput || true

# Запуск gunicorn
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3
