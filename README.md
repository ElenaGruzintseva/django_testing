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

### Чтобы развернуть проект, установите зависимости, примените миграции, загрузите фикстуры, запустите сервер:

```
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures.json
python manage.py runserver
```
