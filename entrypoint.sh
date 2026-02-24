#!/bin/sh

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "Создание суперпользователя (если не существует)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь admin создан')
else:
    print('Суперпользователь уже существует')
EOF

echo "Запуск сервера..."
exec "$@"