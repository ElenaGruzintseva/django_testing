# Django testing

Написаны unittest для *ya_note* и pytest для *ya_news*.

*ya_note* - Записная книжка от Яндекс Практикум, где авторизованный пользователь оставляет заметки.

*ya_news* - Новостной портал от Яндекс Практикум, где авторизованный пользователь публикует комментарии к новостям.

### Чтобы запустить тесты, в директории ya_note выполните:

```
python manage.py test
```

### Чтобы запустить pytest, в директории ya_news выполните:

```
pytest
```

### Чтобы развернуть проект, клонируйте репозиторий, установите зависимости, примените миграции, загрузите фикстуры, запустите сервер:

```
git clone https://github.com/ElenaGruzintseva/django_testing
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures.json
python manage.py runserver
```
