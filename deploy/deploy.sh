#!/bin/sh
set -e

echo "🚀 Запуск миграций..."
python manage.py migrate --noinput

echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "✅ Запуск gunicorn..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
