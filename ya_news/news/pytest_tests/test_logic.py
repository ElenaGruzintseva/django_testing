from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


FORM_DATA = {
    'text': 'Текст комментария.'
}
BAD_WORDS_DATA = {'text': f'Text, {BAD_WORDS[0]}, text'}


@pytest.mark.skip(reason='')
def test_anonymous_user_cant_create_comment(
    client, news_detail_url, news, author
):
    expected_count = list(Comment.objects.all())
    client.post(news_detail_url, data=FORM_DATA)
    assert list(Comment.objects.all()) == expected_count
    with pytest.raises(Comment.DoesNotExist):
        Comment.objects.get(text=FORM_DATA['text'], news=news, author=author)


@pytest.mark.skip(reason='')
def test_user_can_create_comment(news_detail_url, news, author, author_client):
    comments = set(Comment.objects.all())
    assertRedirects(
        author_client.post(news_detail_url, data=FORM_DATA), news_detail_url
    )
    comments_difference = set(Comment.objects.all()).difference(comments)
    assert len(comments_difference) == 1
    comment = comments_difference.pop()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.skip(reason='Лучше протестировать каждое запрещенное слово.')
def test_user_cant_use_bad_words(
        author_client, news_detail_url
):
    comments_count = Comment.objects.count()
    response = author_client.post(news_detail_url, data=BAD_WORDS_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == comments_count


@pytest.mark.skip(reason='')
def test_author_can_edit_comment(
    author_client, comment, news_edit_url, news_detail_url
):
    assertRedirects(
        author_client.post(news_edit_url, FORM_DATA, news_detail_url))
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


@pytest.mark.skip(reason='')
def test_author_can_delete_comment(
    author_client, news_delete_url, news_detail_url, news, author
):
    comment = Comment.objects.create(
        text=FORM_DATA['text'], news=news, author=author
    )
    comments_count = Comment.objects.count()
    assertRedirects(author_client.delete(
        news_delete_url, data={'comment_id': comment.pk}), news_detail_url
    )
    assert Comment.objects.count() == comments_count - 1



# @pytest.mark.skip(reason='Сломана. Не хватает контроля всех записи, которую пытались удалить.')
def test_user_cant_delete_comment_of_another_user(
    reader_client, news_delete_url, news, author
):
    comment = Comment.objects.create(
        text=FORM_DATA['text'], news=news, author=author
    )
    comments_count = Comment.objects.count()
    response = reader_client.delete(news_delete_url, data=comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
    assert Comment.objects.count() == comments_count


@pytest.mark.skip(reason='')
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
