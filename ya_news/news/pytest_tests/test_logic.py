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

# @pytest.mark.skip(reason='Замените на сравнение состава таблицы "до" и "после')
def test_anonymous_user_cant_create_comment(
    client, news_detail_url
):
    comments_count = Comment.objects.count()
    client.post(news_detail_url, data=FORM_DATA)
    assert Comment.objects.count() == comments_count

# @pytest.mark.skip(reason='Все урлы нужно рассчитать один раз заранее, до теста, Не хватает контроля, что создана одна запись')
def test_user_can_create_comment(
        author_client, author, news_detail_url, news
):
    comments_count = Comment.objects.count()
    comments = set(Comment.objects.all())
    response = author_client.post(news_detail_url, data=FORM_DATA)
    assertRedirects(response, f'{news_detail_url}#comments')
    # assert Comment.objects.count() == comments_count + 1
    comments = set(Comment.objects.all()).difference(comments)
    assert len(comments) == 1
    comment = comments.pop()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


# @pytest.mark.skip(reason='Лучше протестировать каждое запрещенное слово.')
def test_user_cant_use_bad_words(
        author_client, news_detail_url
):
    comments_count = Comment.objects.count()
    response = author_client.post(news_detail_url, data=BAD_WORDS_DATA)
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


@pytest.mark.skip(reason='Сломана. Все урлы нужно рассчитать один раз заранее, до теста. Не хватает контроля, что удалилась ожидаемая запись.')
def test_author_can_delete_comment(
    author_client, news_delete_url, news_detail_url
):
    comments_count = Comment.objects.count()
    self.assertEqual(
        author_client.delete(
            news_delete_url).status_code, HTTPStatus.OK
    )
    self.assertIsInstance(self.note, Note)
    note = Note.objects.get(id=self.note.id)
    self.assertEqual(self.note.author, note.author)
    self.assertEqual(self.note.title, note.title)
    self.assertEqual(self.note.text, note.text)
    self.assertEqual(self.note.slug, note.slug)


@pytest.mark.skip(reason='Сломана. Не хватает контроля всех предметных полей записи, которую пытались удалить.')
def test_user_cant_delete_comment_of_another_user(
    reader_client, news_delete_url, comment
):
    assert reader_client.post(news_delete_url, data=FORM_DATA).status_code == HTTPStatus.NOT_FOUND

    assert FORM_DATA.text == comment.text
    assert FORM_DATA.news == comment.news
    assert FORM_DATA.author == comment.author
    assert FORM_DATA.created == comment.created



    # comments_count = Comment.objects.count()
    # response = reader_client.delete(news_delete_url)
    # assert response.status_code == HTTPStatus.NOT_FOUND
    # assert Comment.objects.count() == comments_count


# @pytest.mark.skip(reason='Все урлы нужно рассчитать один раз заранее, до теста, Не хватает контроля, что создана одна запись')
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
