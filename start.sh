#!/usr/bin/env bash
set -e   # migrate ve collectstatic kritik — hata varsa dur

echo "[START] migrate başlıyor..."
python manage.py migrate --noinput

echo "[START] collectstatic başlıyor..."
python manage.py collectstatic --noinput --clear

echo "[START] Gunicorn başlatılıyor..."
exec gunicorn nabiz.wsgi:application \
  --bind "0.0.0.0:${PORT:-8080}" \
  --workers 2 \
  --timeout 120
