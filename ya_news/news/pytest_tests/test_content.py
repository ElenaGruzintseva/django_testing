import pytest

from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_home_url, all_news):
    assert client.get(news_home_url).context[
        'object_list'].count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home_url, all_news):
    all_dates = [news.date for news in client.get(news_home_url)
                 .context['object_list']]
    assert sorted(all_dates, reverse=True) == all_dates


def test_comments_order(client, news_detail_url):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_dates = [comment.created for comment in news.comment_set.all()]
    assert sorted(all_dates) == all_dates


def test_anonymous_client_has_no_form(client, news_detail_url):
    assert 'form' not in client.get(news_detail_url).context


def test_authorized_client_has_form(author_client, news_detail_url):
    response = author_client.get(news_detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
