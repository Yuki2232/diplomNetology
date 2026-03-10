# Fashion Shop API - Документация проекта

## Описание проекта

Backend-часть интернет-магазина одежды и обуви на Django REST Framework. Сервис предоставляет REST API для автоматизации закупок в розничной сети.

### Функциональность
- Регистрация и авторизация пользователей
- Управление товарами (просмотр, фильтрация, поиск)
- Работа с корзиной (добавление/удаление товаров от разных поставщиков)
- Управление адресами доставки
- Оформление и подтверждение заказов
- Email-уведомления
- Импорт товаров из файлов (JSON/CSV)
- Управление магазинами для поставщиков

## Технологии
- Python 3.10/3.11
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- Djoser (аутентификация)
- Django CORS Headers
- Docker & Docker Compose

## Установка и запуск

### Вариант 1: Запуск без Docker

#### 1. Клонирование репозитория
```bash
git clone <url-репозитория>
cd DIPLOM
2. Виртуальное окружение
bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Зависимости
bash
pip install django djangorestframework djoser django-cors-headers django-filter psycopg2-binary python-decouple
4. PostgreSQL
bash
# Вход в PostgreSQL
psql -U postgres
# Создание базы данных
CREATE DATABASE fashion_shop_db;
\q
5. Настройка переменных окружения
Создайте файл .env в корне проекта:

env
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL Database
DB_NAME=fashion_shop_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=test@example.com
ADMIN_EMAIL=admin@example.com
6. Миграции
bash
python manage.py makemigrations users
python manage.py makemigrations shops
python manage.py makemigrations products
python manage.py makemigrations orders
python manage.py migrate
python manage.py createsuperuser
7. Импорт товаров
Создайте data/products.json:

json
[
    {
        "name": "Рубашка классическая",
        "category": "Рубашки",
        "price": 2990.00,
        "quantity": 50,
        "gender": "male"
    },
    {
        "name": "Джинсы скинни",
        "category": "Джинсы",
        "price": 3990.00,
        "quantity": 30,
        "gender": "female"
    }
]
bash
python manage.py import_products --shop=1 --file=data/products.json
8. Запуск
bash
python manage.py runserver
Сервер: http://127.0.0.1:8000/

Вариант 2: Запуск через Docker
1. Клонирование репозитория
bash
git clone <url-репозитория>
cd DIPLOM
2. Настройка переменных окружения
Создайте файл .env в корне проекта (см. пример выше)

3. Запуск Docker Compose
bash
docker-compose up -d --build
4. Применение миграций
bash
docker-compose exec web python manage.py migrate
5. Создание суперпользователя
bash
docker-compose exec web python manage.py createsuperuser
6. Импорт товаров
bash
docker-compose exec web python manage.py import_products --shop=1 --file=data/products.json
7. Открыть приложение
API: http://localhost:8000

Adminer (управление БД): http://localhost:8080

Полезные команды Docker
bash
# Просмотр логов
docker-compose logs -f

# Остановка контейнеров
docker-compose down

# Полная перезагрузка (с удалением БД)
docker-compose down -v
docker-compose up -d --build
Переменные окружения
Файл .env.example
env
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,web
FRONTEND_URL=http://localhost:3000

# PostgreSQL Database
DB_NAME=fashion_shop_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email settings (для разработки)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST_USER=test@example.com
ADMIN_EMAIL=admin@example.com

Описание переменных
Переменная	Описание	По умолчанию
DEBUG	Режим отладки	True
SECRET_KEY	Секретный ключ Django	обязательно изменить!
ALLOWED_HOSTS	Разрешенные хосты	localhost,127.0.0.1,web
FRONTEND_URL	URL фронтенда для ссылок в письмах	http://localhost:3000
DB_NAME	Название базы данных	fashion_shop_db
DB_USER	Пользователь БД	postgres
DB_PASSWORD	Пароль БД	postgres
DB_HOST	Хост БД	db (localhost без Docker)
DB_PORT	Порт БД	5432
CORS_ALLOWED_ORIGINS	Разрешенные источники CORS	http://localhost:3000,http://127.0.0.1:3000
EMAIL_BACKEND	Бэкенд email	console.EmailBackend
EMAIL_HOST_USER	Email отправителя	test@example.com
ADMIN_EMAIL	Email администратора	admin@example.com
API Endpoints
Аутентификация
Метод	Endpoint	Описание
POST	/api/v1/users/register/	Регистрация
POST	/api/v1/users/login/	Авторизация
GET	/api/v1/users/profile/me/	Текущий пользователь
Контакты (требуется токен)
Метод	Endpoint	Описание
POST	/api/v1/users/contacts/	Создать контакт
GET	/api/v1/users/contacts/	Список контактов
DELETE	/api/v1/users/contacts/<id>/	Удалить контакт
Товары
Метод	Endpoint	Описание
GET	/api/v1/products/	Список товаров
GET	/api/v1/products/<id>/	Детали товара
Фильтры:

text
?category=1
&shop=2
&gender=male
&min_price=1000
&max_price=5000
&in_stock=true
&search=рубашка
Корзина (требуется токен)
Метод	Endpoint	Описание
GET	/api/v1/orders/cart/	Просмотр корзины
POST	/api/v1/orders/add_to_cart/	Добавить товар
POST	/api/v1/orders/remove_from_cart/	Удалить товар
Заказы (требуется токен)
Метод	Endpoint	Описание
POST	/api/v1/orders/confirm/	Оформить заказ
GET	/api/v1/orders/	Список заказов
GET	/api/v1/orders/<id>/details/	Детали заказа
PATCH	/api/v1/orders/<id>/update_status/	Изменить статус
Для поставщиков (требуется токен)
Метод	Endpoint	Описание
POST	/api/v1/shops/shops/	Создать магазин
POST	/api/v1/shops/shops/<id>/toggle_status/	Вкл/выкл заказы
GET	/api/v1/shops/categories/	Категории
Примеры запросов
Регистрация
bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "email": "test@test.com",
    "password": "pass123",
    "password2": "pass123"
  }'
Авторизация
bash
curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test",
    "password": "pass123"
  }'
Сохраните полученный токен

Добавление контакта
bash
curl -X POST http://127.0.0.1:8000/api/v1/users/contacts/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Москва",
    "street": "Тверская",
    "house": "10",
    "phone": "+79991234567"
  }'
Добавление в корзину
bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/add_to_cart/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
Подтверждение заказа
bash
curl -X POST http://127.0.0.1:8000/api/v1/orders/confirm/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": 1
  }'
Создание магазина (для поставщиков)
bash
curl -X POST http://127.0.0.1:8000/api/v1/shops/shops/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Мой магазин одежды",
    "url": "https://myshop.ru"
  }'
Включение/отключение приема заказов
bash
curl -X POST http://127.0.0.1:8000/api/v1/shops/shops/1/toggle_status/ \
  -H "Authorization: Token <token>"
Статусы заказа
Статус	Описание
basket	В корзине
new	Новый
confirmed	Подтвержден
assembled	Собран
sent	Отправлен
delivered	Доставлен
canceled	Отменен
Возможные ошибки
ModuleNotFoundError: No module named 'decouple'
bash
pip install python-decouple
Ошибка подключения к PostgreSQL
bash
# Проверьте что PostgreSQL запущен
# Windows: Services -> PostgreSQL -> Запустить
# Mac: brew services start postgresql
# Linux: sudo systemctl start postgresql
Ошибка при импорте товаров
bash
# Проверьте существование магазина
python manage.py shell
from apps.shops.models import Shop
Shop.objects.all()
Ошибка "SECRET_KEY is not set"
bash
# Убедитесь, что в .env файле указан SECRET_KEY
echo "SECRET_KEY=your-secure-random-key" >> .env
Ошибка подключения к БД в Docker
bash
# Проверьте состояние контейнеров
docker-compose ps
# Перезапустите контейнеры
docker-compose down -v
docker-compose up -d --build