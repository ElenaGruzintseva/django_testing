from http import HTTPStatus
import unittest

from pytils.translit import slugify

from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)
# Перенесите алгоритм: запрос, извлечение созданного, контроль полей -
# в новый метод. Вызывайте этот метод из обоих тестов, где проверяется
# успешное создание, это -
# test_user_can_create_note, test_user_can_create_note_without_slug.

class TestLogic(TestBase):

    # @unittest.skip(reason='')
    def test_user_can_create_note(self):
        notes = set(Note.objects.all())
        self.assertRedirects(self.author_client.post(
            URL_NOTES_ADD, data=self.new_created_note), URL_NOTES_SUCCESS
        )
        difference = set(Note.objects.all()) - notes
        self.assertEqual(len(difference), 1)
        new_note = difference.pop()
        self.assertEqual(new_note.title, self.new_created_note['title'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, self.new_created_note['slug'])
        self.assertEqual(new_note.text, self.new_created_note['text'])

    # @unittest.skip(reason='')
    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(URL_NOTES_ADD, data=self.new_created_note)
        self.assertEqual(notes, set(Note.objects.all()))

    @unittest.skip(reason='Не хватает явного кода в этом тесте, копирующего слаг из записи в поле формы.')
    def test_cant_create_note_with_duplicate_slug(self):
        notes = set(Note.objects.all())
        self.author_client.post(
            URL_NOTES_ADD,
            slug=self.note['slug']
        )
        self.assertEqual(set(Note.objects.all()), notes)

    @unittest.skip(reason='Перенесите алгоритм: запрос, извлечение созданного, контроль полей - в новый метод.')
    def test_user_can_create_note_without_slug(self):
        Note.objects.all().delete()
        self.new_created_note.pop('slug')
        response = self.author_client.post(
            URL_NOTES_ADD, data=self.new_created_note
        )
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        created_note = Note.objects.get(title=self.new_created_note['title'])
        self.assertEqual(
            created_note.slug, slugify(self.new_created_note['title'])
        )
        self.assertEqual(created_note.title, self.new_created_note['title'])
        self.assertEqual(created_note.text, self.new_created_note['text'])
        self.assertEqual(created_note.author, self.author)

    # @unittest.skip(reason='')
    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                URL_NOTES_EDIT, data=self.new_created_note
            ).status_code, HTTPStatus.FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.new_created_note['title'])
        self.assertEqual(note.text, self.new_created_note['text'])
        self.assertEqual(note.slug, self.new_created_note['slug'])
        self.assertEqual(note.author, self.note.author)

    # @unittest.skip(reason='')
    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=self.new_created_note
        ).status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    # @unittest.skip(reason='')
    def test_author_can_delete_note(self):
        start_notes_count = Note.objects.count()
        self.author_client.delete(URL_NOTES_DELETE)
        self.assertEqual(start_notes_count, Note.objects.count() + 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    @unittest.skip(reason='Не хватает контроля, что запись еще есть в таблице.')
    def test_user_cant_delete_note_of_another_user(self):
        start_notes_count = Note.objects.count()
        self.assertEqual(
            self.reader_client.delete(
                URL_NOTES_DELETE).status_code, HTTPStatus.NOT_FOUND
        )
        self.assertEqual(start_notes_count, Note.objects.count())
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
