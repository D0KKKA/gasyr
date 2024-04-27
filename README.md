Как запустить проект на Python (для начала установите Python)
На Windows:
Установите Python с официального сайта Python, если его еще нет.

Откройте командную строку (cmd) и перейдите в директорию проекта.

cd gasyrlab/
Создайте виртуальное окружение:

python -m venv venv
venv\Scripts\activate
Установите зависимости:

pip install -r requirements.txt
Выполните миграции базы данных:

cd gasyrlab/
python manage.py makemigrations
python manage.py migrate
Создайте суперпользователя (опционально):

python manage.py createsuperuser

Запустите сервер:

python manage.py runserver
Как использовать проект
После запуска сервера вы сможете открыть приложение в вашем веб-браузере по адресу http://127.0.0.1:8000/.

После запуска сервера и создания суперпользователя можно перейти в админ панель сайта http://127.0.0.1:8000/admin/.

документация http://127.0.0.1:8000/api/swagger.
