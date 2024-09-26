from datetime import datetime, timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

NEWS_COUNT_ON_HOME_PAGE = 10
COMMENTS_COUNT = 10


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def news_delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture(autouse=True)
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture(autouse=True)
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture(autouse=True)
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture(autouse=True)
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture(autouse=True)
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )


@pytest.fixture(autouse=True)
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст'
    )


@pytest.fixture(autouse=True)
def other_comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст',
    )


@pytest.fixture(autouse=True)
def all_news():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture(autouse=True)
def all_comment(news, author):
    now = timezone.now()
    Comment.objects.bulk_create(
        Comment(news=news, author=author, text=f'Tекст {index}',
                created=now + timedelta(days=index))
        for index in range(COMMENTS_COUNT)
    )