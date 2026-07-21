## LMS (Learning Management System)

Платформа для онлайн-обучения, где каждый желающий может размещать свои материалы или курсы.

---

## Технологии

- Python 3.13
- Django 6.0
- Django REST Framework (DRF)
- PostgreSQL
- Redis (брокер сообщений / кэш)
- Celery (асинхронные задачи)
- Celery Beat (периодические задачи)
- Stripe (платежи)
- JWT (authentication via `rest_framework_simplejwt`)
- Docker / Docker Compose
- Swagger / OpenAPI (drf-yasg)
- django-filter (фильтрация)
- forex-python (конвертация валют)

---

## Структура проекта

```
├── config/                  # Настройки Django
│   ├── settings.py          # Конфигурация проекта
│   ├── urls.py              # Корневые URL
│   ├── celery.py            # Настройки Celery
│   ├── asgi.py / wsgi.py    # ASGI/WSGI точки входа
├── lms/                     # Приложение "Курсы и уроки"
│   ├── models.py            # Course, Lesson, CourseSubscription
│   ├── views.py             # ViewSets / Generic views
│   ├── serializers.py       # Сериализаторы
│   ├── services.py          # Бизнес-логика
│   ├── tasks.py             # Celery-задачи
│   ├── validators.py        # Валидация ссылок
│   ├── paginators.py        # Пагинация
│   ├── tests.py             # Тесты
│   └── urls.py              # Маршруты lms
├── users/                   # Приложение "Пользователи и платежи"
│   ├── models.py            # User, Payment
│   ├── views.py             # CRUD пользователей, платежи Stripe
│   ├── serializers.py       # Сериализаторы
│   ├── services.py          # Stripe API, конвертация валют
│   ├── permissions.py       # Права доступа
│   ├── urls.py              # Маршруты users
│   └── management/commands/ # Кастомные manage.py команды
├── static/                  # Статические файлы
├── media/                   # Медиафайлы (загрузки)
├── .env                     # Переменные окружения (локально)
├── .env.docker              # Переменные окружения (Docker)
├── .env.example             # Пример .env
├── docker-compose.yaml      # Docker Compose
├── Dockerfile               # Docker образ
├── requirements.txt         # Зависимости
├── pyproject.toml           # Конфигурация проекта
└── manage.py                # Точка входа Django
```

---

## Модели

**Пользователь** (`users.User`)
- Авторизация по email (вместо username)
- Телефон, город, аватарка

**Курс** (`lms.Course`)
- Название, превью, описание, ссылка на видео, цена
- Владелец (FK на User)

**Урок** (`lms.Lesson`)
- Название, описание, превью, ссылка на видео
- Курс (FK) + владелец (FK на User)

**Подписка на курс** (`lms.CourseSubscription`)
- Пользователь + курс (unique together)

**Платеж** (`users.Payment`)
- Пользователь, курс/урок, сумма, метод, session_id (Stripe), статус

---

## Файлы окружения

Проект использует два файла для переменных окружения:

| Файл | Использование | DB_HOST |
|------|---------------|---------|
| `.env` | Локальный запуск | `localhost` |
| `.env.docker` | Docker Compose | `db` |

Оба файла добавлены в `.gitignore` и не попадают в репозиторий.

### Настройка `.env` (локальный запуск)

1. Скопировать пример:
   ```bash
   cp .env.example .env
   ```

2. Отредактировать `.env`, указав свои данные БД:
   ```env
   POSTGRES_DB=drf
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

3. Для Stripe payments:
   ```env
   STRIPE_API_KEY=sk_test_...
   ```

4. Для email-уведомлений:
   ```env
   EMAIL_HOST_USER=your@email.com
   EMAIL_HOST_PASSWORD=your_password
   ```

### Настройка `.env.docker` (Docker)

Файл `.env.docker` создаётся автоматически при необходимости. Отличается от локального только:
- `DB_HOST=db` (имя сервиса в docker-compose)
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/0`

---

## Запуск проекта

### Локально

**Требования:**
- Python 3.13+
- PostgreSQL (запущенный на localhost:5432)
- Redis (опционально, для Celery)

**Шаги:**

1. Клонировать репозиторий:
   ```bash
   git clone <repository-url>
   cd Online_training_DRF
   ```

2. Настроить `.env` (см. раздел "Файлы окружения").

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создать базу данных в PostgresSQL:
   ```bash
   createdb drf
   ```

5. Применить миграции:
   ```bash
   python manage.py migrate
   ```

6. Запустить сервер разработки:
   ```bash
   python manage.py runserver
   ```

   Сервер будет доступен по адресу: http://localhost:8000/

7. (Опционально) Запустить Celery для асинхронных задач:
   ```bash
   # В отдельном терминале — воркер
   celery -A config worker -l INFO

   # В отдельном терминале — планировщик периодических задач
   celery -A config beat -l INFO -S django
   ```

8. (Опционально) Создать суперпользователя:
   ```bash
   python manage.py create_superuser
   ```

   Админка: http://localhost:8000/admin/

### Пример после запуска

После запуска сервера (локально или в Docker) доступны следующие эндпоинты:

**Аутентификация:**

```bash
# Получить JWT токен
curl -X POST http://localhost:8000/users/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin12345"}'

# Обновить токен
curl -X POST http://localhost:8000/users/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

**Пользователи:**

```bash
# Регистрация
curl -X POST http://localhost:8000/users/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword123"}'

# Список пользователей (требуется JWT)
curl http://localhost:8000/users/ \
  -H "Authorization: Bearer <access_token>"
```

**Курсы:**

```bash
# Список курсов
curl http://localhost:8000/courses/ \
  -H "Authorization: Bearer <access_token>"

# Детальная информация о курсе (с уроками и подпиской)
curl http://localhost:8000/courses/1/ \
  -H "Authorization: Bearer <access_token>"

# Создать курс
curl -X POST http://localhost:8000/courses/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Python для начинающих", "description": "Базовый курс Python", "price": 15000}'
```

**Подписка на курс:**

```bash
# Подписаться / отписаться (toggle)
curl -X POST http://localhost:8000/subscribe/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"course": 1}'
```

**Платежи:**

```bash
# Создать платеж (возвращает session_id и payment_link от Stripe)
curl -X POST http://localhost:8000/payment/pay/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"course": 1, "payment_method": "transfer"}'

# Проверить статус платежа
curl http://localhost:8000/payment/status/1/ \
  -H "Authorization: Bearer <access_token>"
```

**Документация:**

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Админка: http://localhost:8000/admin/

### Через Docker

**Требования:**
- Docker
- Docker Compose

**Шаги:**

1. Собрать и запустить все сервисы:
   ```bash
   docker compose up -d --build
   ```

2. Проверить статус контейнеров:
   ```bash
   docker compose ps
   ```

3. Создать суперпользователя:
   ```bash
   docker compose exec web python manage.py create_superuser
   ```

4. Для просмотра логов:
   ```bash
   docker compose logs -f
   ```

5. Остановить проект:
   ```bash
   docker compose down
   ```

   Полная очистка (с удалением томов БД):
   ```bash
   docker compose down --volumes
   ```

---

## Запуск тестов

### Все тесты

```bash
python manage.py test
```

### Тесты конкретного приложения

```bash
# Только lms
python manage.py test lms

# Только users
python manage.py test users
```

### С coverage-отчётом

```bash
# Установить coverage
pip install coverage

# Запустить тесты с замером покрытия
coverage run manage.py test

# Показать отчёт в терминале
coverage report

# Создать HTML-отчёт (открыть htmlcov/index.html)
coverage html
```

### В Docker

```bash
docker compose exec web python manage.py test
```

---

## Права доступа

- **Модератор** — просмотр и редактирование любых уроков и курсов, без удаления и создания
- **Владелец** — полный доступ к своим объектам
- **Аутентифицированный пользователь** — базовый доступ

---

## Валидация

Ссылки на видео разрешены только с **youtube.com** (проверка через `YoutubeChanelValidator`).

---

## Платежи (Stripe)

Оплата курсов через Stripe Checkout Session:
- Создание продукта и цены в Stripe
- Конвертация RUB → USD (forex-python)
- Проверка статуса платежа

---

## Документация API

Swagger доступен после запуска:
- `/swagger/` — Swagger UI
- `/redoc/` — ReDoc
