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

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <url-репозитория>
cd DIPLOM

2. Виртуальное окружение
    python -m venv venv
    # Windows:
        venv\Scripts\activate
    # Mac/Linux:
        source venv/bin/activate

3. Зависимости
    pip install django djangorestframework djoser django-cors-headers django-filter psycopg2-binary python-decouple

4. PostgreSQL
    # Вход в PostgreSQL
        psql -U postgres
    # Создание базы данных
    CREATE DATABASE fashion_shop_db;
    \q

5. Миграции
    python manage.py makemigrations users
    python manage.py makemigrations shops
    python manage.py makemigrations products
    python manage.py makemigrations orders
    python manage.py migrate
    python manage.py createsuperuser

6. Импорт товаров
    Создайте data/products.json:
        [
    {
        "name": "Рубашка классическая",
        "category": "Рубашки",
        "price": 2990.00,
        "quantity": 50,
        "gender": "male"
    }
    ]
    python manage.py import_products --shop=1 --file=data/products.json

7. Запуск
    python manage.py runserver
    Сервер: http://127.0.0.1:8000/

-- API Endpoints:
Аутентификация:
    POST   /api/v1/users/register/           # Регистрация
    POST   /api/v1/users/login/               # Авторизация
    GET    /api/v1/users/profile/me/          # Текущий пользователь

Контакты (требуется токен):
    POST   /api/v1/users/contacts/            # Создать контакт
    GET    /api/v1/users/contacts/            # Список контактов
    DELETE /api/v1/users/contacts/<id>/       # Удалить контакт

Товары:
    GET    /api/v1/products/                   # Список товаров
    GET    /api/v1/products/<id>/              # Детали товара

    Фильтры: ?category=1&shop=2&gender=male&min_price=1000&max_price=5000&in_stock=true&search=рубашка

Корзина (требуется токен):

    GET    /api/v1/orders/cart/                 # Просмотр корзины
    POST   /api/v1/orders/add_to_cart/          # Добавить товар
    POST   /api/v1/orders/remove_from_cart/     # Удалить товар

Заказы (требуется токен):

    POST   /api/v1/orders/confirm/              # Оформить заказ
    GET    /api/v1/orders/                       # Список заказов
    GET    /api/v1/orders/<id>/details/          # Детали заказа
    PATCH  /api/v1/orders/<id>/update_status/    # Изменить статус

Для поставщиков (требуется токен):

    POST   /api/v1/shops/shops/                  # Создать магазин
    POST   /api/v1/shops/shops/<id>/toggle_status/ # Вкл/выкл заказы
    GET    /api/v1/shops/categories/              # Категории

--Примеры запросов:

Регистрация:

    curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
        -H "Content-Type: application/json" \
        -d '{"username":"test","email":"test@test.com","password":"pass123","password2":"pass123"}'

Авторизация:

    curl -X POST http://127.0.0.1:8000/api/v1/users/login/ \
        -H "Content-Type: application/json" \
        -d '{"username":"test","password":"pass123"}'    

Добавление контакта:

    curl -X POST http://127.0.0.1:8000/api/v1/users/contacts/ \
        -H "Authorization: Token <token>" \
        -H "Content-Type: application/json" \
        -d '{"city":"Москва","street":"Тверская","house":"10","phone":"+79991234567"}'

Добавление в корзину:

    curl -X POST http://127.0.0.1:8000/api/v1/orders/add_to_cart/ \
        -H "Authorization: Token <token>" \
        -H "Content-Type: application/json" \
        -d '{"product_id":1,"quantity":2}'

Подтверждение заказа:

    curl -X POST http://127.0.0.1:8000/api/v1/orders/confirm/ \
        -H "Authorization: Token <token>" \
        -H "Content-Type: application/json" \
        -d '{"contact_id":1}'

Статусы заказа:

    -basket - В корзине

    -new - Новый

    -confirmed - Подтвержден

    -assembled - Собран

    -sent - Отправлен

    -delivered - Доставлен

    -canceled - Отменен

Возможные ошибки:

    ModuleNotFoundError: No module named 'decouple'

        -pip install python-decouple

Ошибка подключения к PostgreSQL:

    # Проверьте что PostgreSQL запущен
    # Windows: Services -> PostgreSQL -> Запустить
    # Mac: brew services start postgresql
    # Linux: sudo systemctl start postgresql

Ошибка при импорте товаров:
    # Проверьте существование магазина
    python manage.py shell
    from apps.shops.models import Shop
    Shop.objects.all()






    