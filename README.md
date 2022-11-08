# FOODGRAM - Незаменимый продуктовый помощник для любой хозяйки.
___
Сервис для обмена вашимих любимых рецептов на любимые рецепты других пользователей.

## Используемые технологии
___
- Django 
- Django Rest Framework 
- Docker 
- Docker-compose 
- Gunicorn 
- Nginx 
- PostgreSQL

## Workflow
____
- **tests**: Проверка кода на соответствие PEP8. 
- **push** Docker image to Docker Hub: Сборка и публикация образа на DockerHub. 
- **deploy**: Автоматический деплой на боевой сервер при пуше в главную ветку main. 
- **send_massage**: Отправка уведомления в телеграм-чат.

## Запуск проекта
___
- Склонируйте репозиторий с проектом:

```git clone git@github.com/naelsa/foodgram-project-react```

### ЛОКАЛЬНЫЙ ЗАПУСК ПРОЕКТА
___

<details>

- Перейдите в папку с настройками бэкенда проекта:

`  \foodgram-project-react\backend\foodgram
`
- Установите и активируйте виртуальное окружение.

`python -m venv venv source venv/Scripts/activate`

- Перейдите в папку с проектом

`cd \foodgram-project-react\backend`

- Установите зависимости из файла requirements.txt:

`python -m pip install --upgrade pip
pip install -r requirements.txt`

- Выполните последовательно следующие команды:

```python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py createsuperuser
```

</details>

## WORKFLOW и .env

----

<details>

- Для работы с Workflow добавить в Secrets GitHub переменные окружения:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID своего телеграм-аккаунта>
TELEGRAM_TOKEN=<токен вашего бота>
```
- .env

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

SECRET_KEY=<secret key>

ALLOWED_HOSTS=<allowed hosts>

DEBUG=<False or True>

CSRF_TRUSTED_ORIGINS='http://localhost, http://127.0.0.1'

```

</details>