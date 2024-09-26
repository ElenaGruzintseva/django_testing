from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


FORM_DATA = {
    'text': 'Текст комментария.'
}


def test_anonymous_user_cant_create_comment(
    client, news_detail_url
):
    comments_count = Comment.objects.count()
    client.post(news_detail_url, data=FORM_DATA)
    assert Comment.objects.count() == comments_count


def test_user_can_create_comment(
        author_client, author, news_detail_url, news
):
    comments_count = Comment.objects.count()
    comments_all = set(Comment.objects.all())
    response = author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == comments_count + 1
    comments_upd_all = set(Comment.objects.all())
    comments_difference = comments_upd_all.difference(comments_all)
    assert len(comments_difference) == 1
    comment = comments_difference.pop()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(
        author_client, news_detail_url
):
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'Text, {BAD_WORDS[0]}, text'}
    response = author_client.post(news_detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(
    author_client, comment, news_edit_url, news_detail_url
):
    assertRedirects(
        author_client.post(news_edit_url, FORM_DATA),
        f'{news_detail_url}#comments'
    )
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_author_can_delete_comment(
    author_client, news_delete_url, news_detail_url
):
    comments_count = Comment.objects.count()
    response = author_client.delete(news_delete_url)
    assertRedirects(response, f'{news_detail_url}#comments')
    assert Comment.objects.count() == comments_count - 1


def test_user_cant_delete_comment_of_another_user(
    reader_client, news_delete_url
):
    comments_count = Comment.objects.count()
    response = reader_client.delete(news_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


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
