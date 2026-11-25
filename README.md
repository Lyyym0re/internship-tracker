# Internship Tracker

API для учёта откликов на стажировки. Можно сохранить отклик, посмотреть список, отфильтровать его по статусу, обновить статус и удалить запись.

Приложение написано на Python и FastAPI. Данные хранятся в PostgreSQL. Обработчики выполняют запросы через общий асинхронный пул psycopg 3, который открывается при запуске и закрывается при остановке сервера.

| Метод | Маршрут | Действие |
| --- | --- | --- |
| POST | `/applications` | Создать отклик со статусом `applied`. Ответ `201` |
| GET | `/applications` | Получить список. Пример фильтра: `?status=interview` |
| GET | `/applications/{application_id}` | Получить отклик по ID |
| PATCH | `/applications/{application_id}` | Изменить статус отклика |
| DELETE | `/applications/{application_id}` | Удалить отклик. Ответ `204` без тела |

Допустимые статусы — `applied`, `interview`, `offer` и `rejected`.

## Локальный запуск на Windows

Понадобятся Python 3.13, запущенный PostgreSQL и утилита `psql`. Выполняй команды в PowerShell из корня проекта.

**1. Создай виртуальное окружение и установи зависимости.**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**2. Создай базу и таблицу откликов.**

В примере используется локальная роль `postgres`. Если у тебя другая роль с правом создавать базы и таблицы, подставь её здесь и в строке подключения.

```powershell
psql -h localhost -U postgres -d postgres -c "CREATE DATABASE internship_tracker;"
psql -h localhost -U postgres -d internship_tracker -v ON_ERROR_STOP=1 -c (Get-Content -Raw app/sql/schema.sql)
```

Если база уже создана, пропусти первую команду. Схему примени один раз, пока таблицы `applications` в базе ещё нет.

**3. Настрой подключение и запусти сервер.**

Создай локальный файл `app/.env` и задай строку подключения. Замени `example_password` своим паролем. Специальные символы в пароле нужно закодировать для URL. Файл с реальными настройками исключён из Git.

```dotenv
DATABASE_URL=postgresql://postgres:example_password@localhost:5432/internship_tracker
```

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --env-file app/.env
```

`--env-file` загружает `DATABASE_URL` из файла. В Uvicorn 0.54.0 на Windows режим `--reload` выбирает цикл событий `SelectorEventLoop`, совместимый с асинхронным psycopg.

Открой [Swagger UI](http://127.0.0.1:8000/docs).

## Пробный сценарий

1. Вызови `POST /applications` и передай `{"company": "Example Bank", "position": "Python Intern"}`. Ожидай `201` и статус `applied`. Сохрани полученный ID.
2. Вызови `PATCH /applications/{application_id}` с этим ID и телом `{"status": "interview"}`.
3. Проверь новый статус через `GET /applications/{application_id}`. Созданный отклик также должен быть в `GET /applications?status=interview`.
4. Удали отклик через `DELETE /applications/{application_id}`. Ожидай `204` без тела, а при следующем GET по тому же ID — `404`.

## Структура проекта

- `app/main.py` — создание FastAPI, подключение роутера и управление пулом.
- `app/api/applications.py` — HTTP-маршруты откликов.
- `app/models.py` — модели запросов и ответов.
- `app/storage.py` — параметризованные SQL-запросы через psycopg.
- `app/sql/schema.sql` — схема таблицы откликов.
- `tests/` — автоматические проверки.

## Запуск тестов

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

