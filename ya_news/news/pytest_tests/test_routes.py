from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


ANONYMOUS_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
READER_CLIENT = pytest.lazy_fixture('reader_client')
URL_HOME = pytest.lazy_fixture('news_home_url')
URL_NEWS_DETAIL = pytest.lazy_fixture('news_detail_url')
URL_LOGIN = pytest.lazy_fixture('users_login_url')
URL_LOGOUT = pytest.lazy_fixture('users_logout_url')
URL_SIGNUP = pytest.lazy_fixture('users_signup_url')
URL_EDIT_COMMENT = pytest.lazy_fixture('news_edit_url')
URL_DELETE_COMMENT = pytest.lazy_fixture('news_delete_url')
COMMENT_DETAIL_URL = pytest.lazy_fixture('comment_detail_url')
URL_EDIT_REDIRECT = pytest.lazy_fixture('url_edit_redirect')
URL_DELETE_REDIRECT = pytest.lazy_fixture('url_delete_redirect')


@pytest.mark.parametrize(
    'urls, parametrized_client, expected_status',
    (
        (URL_HOME, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_LOGIN, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (COMMENT_DETAIL_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_EDIT_REDIRECT, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_DELETE_REDIRECT, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, ANONYMOUS_CLIENT, HTTPStatus.FOUND),
        (URL_DELETE_COMMENT, ANONYMOUS_CLIENT, HTTPStatus.FOUND),

        (URL_HOME, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_LOGIN, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DETAIL_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DELETE_COMMENT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_EDIT_REDIRECT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DELETE_REDIRECT, AUTHOR_CLIENT, HTTPStatus.OK),

        (URL_HOME, READER_CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, READER_CLIENT, HTTPStatus.OK),
        (URL_LOGIN, READER_CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, READER_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, READER_CLIENT, HTTPStatus.OK),
        (COMMENT_DETAIL_URL, READER_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_DELETE_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_EDIT_REDIRECT, READER_CLIENT, HTTPStatus.OK),
        (URL_DELETE_REDIRECT, READER_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_DELETE_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
    ),
)
def test_pages_availability_users(urls, parametrized_client, expected_status):
    assert parametrized_client.get(urls).status_code == expected_status


@pytest.mark.parametrize(
    'urls, parametrized_client, excepted_status',
    (
        (URL_EDIT_COMMENT, ANONYMOUS_CLIENT, URL_EDIT_REDIRECT),
        (URL_DELETE_COMMENT, ANONYMOUS_CLIENT, URL_DELETE_REDIRECT)
    )
)
def test_redirects(urls, parametrized_client, excepted_status):
    assertRedirects(parametrized_client.get(urls), excepted_status)
