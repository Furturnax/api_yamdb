## Развёртывание проекта:
+ Клонировать репозиторий и перейти в него в командной строке:
```shell script
git clone git@github.com:Furturnax/api_yamdb.git
```

```shell script
cd api_yamdb/
```

+ Cоздать и активировать виртуальное окружение (Windows/Bash):
```shell script
python -m venv venv
```

```shell script
source venv/Scripts/activate
```

+ Установить зависимости из файла requirements.txt:
```shell script
python -m pip install --upgrade pip
```

```shell script
pip install -r requirements.txt
```

+ Перейти в директорию с manage.py:
```shell script
cd api_yamdb/
```

+ Выполнить миграции:
```shell script
python manage.py migrate
```

+ Запустить проект:
```shell script
python manage.py runserver
```

<br>

## Схема базы данных:
<img src="./assets/db_schema.png" alt="Schema of db">

<br>

## Порядок загрузки CSV в базу данных:
+ Перейти в директорию с manage.py:
```shell script
cd api_yamdb/
```

+ Запустить загрузку:
```shell script
python manage.py load_csv
```

<br>

## Порядок запросов к API:
Для работы понадобится программа **Postman**. Она существует в `desktop` и `web` версии. Она удобна функционалом. Либо использовать стандартный интерфейс `DRF` без установки дополнительного ПО. 

Запустить проект. По адресу http://127.0.0.1:8000/redoc/ будет доступна документация для API **YaMDb**. В документации описано, как работает API. Документация представлена в формате **Redoc**.

Зарегистрировать пользователя через Admin-панель.
+ Перейти в директорию с manage.py:
```shell script
cd api_yamdb/
```

+ Создать пользователя-администратора:
```shell script
python manage.py createsuperuser
```

Получить JWT-токен через **Postman**.  
+ По адресу http://127.0.0.1:8000/api/v1/auth/signup/, через POST запрос передать данные в формате `JSON`:
```
{
    "email": "email",
    "username": "username"
}
```

Получаем письмо в директорию `sent_emails` и в строке "Код для подтверждения регистрации:"
копируем код (пример возможного кода: bz60db-a8b453b023ee08af8cc1d7cb92109253).

+ По адресу http://127.0.0.1:8000/api/v1/auth/token/, полученный код (пример ниже) передаём в формате`JSON`:
```
{
    "username": "username",
    "confirmation_code": "bz60db-a8b453b023ee08af8cc1d7cb92109253"
}
```
+ и получаем `токен`:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNDQyOTM4LCJpYXQiOjE3MDEzNTY1MzgsImp0aSI6ImZiN2Y5ZTYwYTNiMzQxMzU5NGJlYjc2YTBkNWE0YzlmIiwidXNlcl9pZCI6M30._h5--Xdayja6eMHENZnbRA50XMR7H8b-UQYTqYyaSdc
```

Авторизировать токен во вкладке **Authorization**.
- В разделе **Type** выбрать `Bearer token`;
- В разделе **Token** вставить полученный `токен`;
- Выполнять запросы к `API`, описанных в документации. 

Начать делать запросы согласно документации.