# Internship Tracker

API для учёта откликов на стажировки. Позволяет сохранять отклики, просматривать их и отслеживать переход от подачи заявки до собеседования, оффера или отказа.

Стек проекта — Python, FastAPI, PostgreSQL, psycopg 3 и pytest.

| Метод | Маршрут | Действие |
| --- | --- | --- |
| POST | `/applications` | Создать отклик с начальным статусом `applied` |
| GET | `/applications` | Показать отклики. Можно передать `?status=interview` |
| GET | `/applications/{application_id}` | Получить отклик по ID |
| PATCH | `/applications/{application_id}` | Изменить статус отклика |

Допустимые статусы — `applied`, `interview`, `offer` и `rejected`.

## Локальный запуск

Понадобятся Python 3.13, запущенный PostgreSQL и утилита `psql`. Команды ниже рассчитаны на PowerShell и выполняются из корня проекта.

**1. Создай виртуальное окружение и установи зависимости.**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**2. Создай базу и таблицу откликов.**

В командах используется локальная роль `postgres`. Если у тебя другая роль, которая может создавать базы и таблицы, подставь её имя здесь и в строке подключения.

```powershell
psql -h localhost -U postgres -d postgres -c "CREATE DATABASE internship_tracker;"
psql -h localhost -U postgres -d internship_tracker -v ON_ERROR_STOP=1 -c (Get-Content -Raw app/sql/schema.sql)
```

Если база уже существует, пропусти первую команду. Схему нужно применить один раз к пустой базе.

**3. Задай строку подключения и запусти приложение.**

Замени `example_password` паролем локальной роли PostgreSQL. Если в пароле есть специальные символы URL, их нужно закодировать. Храни реальный пароль вне репозитория.

```powershell
$env:DATABASE_URL = 'postgresql://postgres:example_password@localhost:5432/internship_tracker'
.\.venv\Scripts\python.exe -m uvicorn app.main:app
```

Открой [документацию API](http://127.0.0.1:8000/docs).

## Первый запрос

В Swagger UI вызови `POST /applications` и отправь JSON:

```json
{
  "company": "Example Bank",
  "position": "Python Intern"
}
```

Ответ `201 Created` содержит ID нового отклика и статус `applied`. Используй этот ID в `GET /applications/{application_id}`, затем отправь `{"status": "interview"}` в `PATCH /applications/{application_id}`. После обновления отклик должен появиться в `GET /applications?status=interview`.

## Структура проекта

- `app/main.py` — приложение FastAPI и маршруты.
- `app/models.py` — модели запросов и ответов.
- `app/storage.py` — SQL-запросы через psycopg.
- `app/db.py` — подключение к PostgreSQL.
- `app/sql/schema.sql` — схема таблицы откликов.
- `tests/test_applications.py` — тест маршрута обновления статуса.

## Тесты

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Тест PATCH подменяет функцию обновления и проверяет HTTP-ответ и однократный вызов функции. Для этого теста подключение к PostgreSQL не требуется.

