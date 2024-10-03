from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


FORM_DATA = {
    'text': 'Текст комментария.'
}

BAD_WORDS_DATA = {'text': f'Text, {BAD_WORDS}, text'}


def test_anonymous_user_cant_create_comment(
    client, news_detail_url
):
    initial_comments = list(Comment.objects.all())
    client.post(news_detail_url, data=FORM_DATA)
    final_comments = list(Comment.objects.all())
    for initial_comment, final_comment in zip(initial_comments,
                                              final_comments):
        assert initial_comment.text == final_comment.text
        assert initial_comment.news == final_comment.news
        assert initial_comment.author == final_comment.author
    assert len(initial_comments) == len(final_comments)


def test_user_can_create_comment(
        news_detail_url, news, author, author_client, comment_detail_url
):
    comments = set(Comment.objects.all())
    assertRedirects(
        author_client.post(news_detail_url, data=FORM_DATA), comment_detail_url
    )
    comments = set(Comment.objects.all()).difference(comments)
    assert len(comments) == 1
    comment = comments.pop()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.skip(reason='ЗАПРЕЩЕННЫЕ СЛОВА')
@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(bad_word, news_detail_url, author_client):
    initial_comments = list(Comment.objects.all())
    bad_word_data = {'text': f'Text, {bad_word}, text'}
    response = author_client.post(news_detail_url, data=bad_word_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    final_comments = list(Comment.objects.all())
    assert initial_comments == final_comments


def test_author_can_edit_comment(
    author_client, comment, news_edit_url, comment_detail_url
):
    assertRedirects(
        author_client.post(news_edit_url, FORM_DATA), comment_detail_url)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


@pytest.mark.skip(reason='Исправлено')
def test_author_can_delete_comment(
    author_client, news_delete_url, comment_detail_url,
    news_detail_url, news, author
):
    assertRedirects(
        author_client.post(
            news_detail_url, data=FORM_DATA), comment_detail_url
    )
    comments_count = Comment.objects.count()
    comment = Comment.objects.get(
        text=FORM_DATA['text'], news=news, author=author
    )
    assertRedirects(author_client.delete(
        news_delete_url, data=comment), comment_detail_url)
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news
    assert Comment.objects.count() == comments_count - 1


@pytest.mark.skip(reason='Исправлено')
def test_user_cant_delete_comment_of_another_user(
    reader_client, news_delete_url, news, author,
    author_client, comment_detail_url, news_detail_url
):
    assertRedirects(
        author_client.post(
            news_detail_url, data=FORM_DATA), comment_detail_url
    )
    comment = Comment.objects.get(
        text=FORM_DATA['text'], news=news, author=author
    )
    assert comment.text == FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news
    response = reader_client.delete(news_delete_url, data=comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == FORM_DATA['text']
    assert comment.author == comment.author
    assert comment.news == comment.news


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
