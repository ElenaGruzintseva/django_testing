from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import WARNING
from news.models import Comment
from news.forms import BAD_WORDS

pytestmark = pytest.mark.django_db

FORM_DATA = {
    'text': 'Текст комментария.'
}

BAD_WORDS_DATA = {'text': ' '.join(BAD_WORDS)}


def test_anonymous_user_cant_create_comment(
    client, news_detail_url
):
    initial_comments = set(Comment.objects.all())
    client.post(news_detail_url, data={'text': FORM_DATA['text']})
    assert initial_comments == set(Comment.objects.all())
    assert not Comment.objects.filter(text=FORM_DATA['text']).exists()


def test_user_can_create_comment(
        news_detail_url, news, author, author_client, comment_detail_url
):
    comments = set(Comment.objects.all())
    assertRedirects(
        author_client.post(news_detail_url, data=FORM_DATA), comment_detail_url
    )
    comments = set(Comment.objects.all()) - comments
    assert len(comments) == 1
    comment = comments.pop()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(
    author_client, news_detail_url
):
    initial_comments = set(Comment.objects.all())
    response = author_client.post(news_detail_url, data=BAD_WORDS_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert initial_comments == set(Comment.objects.all())
    assert not Comment.objects.filter(text=FORM_DATA['text']).exists()


def test_author_can_edit_comment(
    author_client, comment, news_edit_url, comment_detail_url
):
    assertRedirects(
        author_client.post(news_edit_url, FORM_DATA), comment_detail_url)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_author_can_delete_comment(
    author_client, news_delete_url, comment_detail_url,
    comment
):
    expected_count = Comment.objects.count() - 1
    assertRedirects(
        author_client.delete(news_delete_url, comment),
        comment_detail_url
    )
    assert expected_count == Comment.objects.count()
    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_user_cant_delete_comment_of_another_user(
    reader_client, news_delete_url, comment
):
    expected_count = Comment.objects.count()
    response = reader_client.delete(news_delete_url, data=comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_count == Comment.objects.count()
    assert Comment.objects.filter(pk=comment.pk).exists()
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment, news_edit_url
):
    assert reader_client.post(
        news_edit_url, FORM_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
