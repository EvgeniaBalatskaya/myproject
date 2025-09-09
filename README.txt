# 🎓 LMS API (Django + DRF)

## 📌 Описание
Проект представляет собой **API для LMS (Learning Management System)**, реализованный на Django REST Framework.  
Система поддерживает работу с пользователями, курсами, уроками и платежами.  

Функционал включает:
- Регистрацию и авторизацию пользователей по email
- Управление курсами и уроками
- Создание и просмотр платежей
- Ограничения по ролям: **владелец, модератор, админ**
- Покрытие тестами основных сценариев

---

## 🚀 Технологии
- Python 3.11+
- Django 5.x
- Django REST Framework
- PostgreSQL / SQLite (по выбору)
- Pytest / Django TestCase для тестов

---

## ⚙️ Установка и запуск

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/EvgeniaBalatskaya/myproject.git
   cd myproject

2. Создать и активировать виртуальное окружение:

python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows

3. Установить зависимости:

pip install -r requirements.txt

4. Создать .env файл по примеру:

cp .env_template .env

5. Выполнить миграции:

python manage.py migrate

6. Создать суперпользователя:

python manage.py createsuperuser

7. Запустить сервер:

python manage.py runserver

8. Запуск воркера
celery -A config worker -l info

# Запуск beat (планировщик)
celery -A config beat -l info

## 📡 API эндпоинты

Пользователи

POST /users/ — регистрация

GET /users/{id}/ — профиль

GET /users/ — список пользователей (для админов)

POST /auth/token/ — получение JWT токена

Курсы и уроки

GET /courses/ — список курсов

POST /courses/ — создание курса (только авторизованные)

PATCH /courses/{id}/ — редактирование курса (владелец или модератор)

DELETE /courses/{id}/ — удаление курса (владелец или админ)

GET /lessons/ — список уроков

POST /lessons/ — создание урока (только авторизованные)

Платежи

GET /payments/ — список платежей

POST /payments/ — создание платежа

GET /payments/{id}/ — детализация платежа

## 🛡️ Права доступа

Владелец: полный доступ к своим объектам

Модератор: может редактировать курсы/уроки, но не удалять

Админ: полный доступ ко всем объектам

Остальные пользователи: только просмотр

## Тестирование

Запуск тестов:

pytest

## Структура проекта
project/
├── lms/                # Приложение для курсов и уроков
├── users/              # Приложение для пользователей и платежей
├── manage.py
├── requirements.txt
├── .env_template
└── README.md


