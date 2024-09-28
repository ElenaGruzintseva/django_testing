from http import HTTPStatus
import unittest

from pytils.translit import slugify

from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)


class CreatedNote(TestBase):

    def method_created_note(self):
        notes = set(Note.objects.all())
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.new_created_note),
            URL_NOTES_SUCCESS)
        difference = set(Note.objects.all()) - notes
        self.assertEqual(len(difference), 1)
        note = difference.pop()
        self.assertEqual(note.title, self.new_created_note['title'])
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.new_created_note['slug'])
        self.assertEqual(note.text, self.new_created_note['text'])


class TestLogic(CreatedNote):

    def test_user_can_create_note(self):
        print(f'НАШ ТЕСТ ТУТ!')
        super().method_created_note()

    @unittest.skip(reason='Перенесите алгоритм: запрос, извлечение созданного, контроль полей - в новый метод.')
    def test_user_can_create_note_without_slug(self):
        super().method_created_note()
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.new_created_note),
            URL_NOTES_SUCCESS)
        new_note2 = Note.objects.get(self.new_created_note)
        new_note2.pop('slug')

        self.assertEqual(slugify(new_note2['title']), new_note2.slug)

        # response = self.author_client.post(
        #     URL_NOTES_ADD, data=self.new_created_note
        # )
        # self.assertRedirects(response, URL_NOTES_SUCCESS)
        # created_note = Note.objects.get(title=self.new_created_note['title'])
        # self.assertEqual(
        #     created_note.slug, slugify(self.new_created_note['title'])
        # )
        # self.assertEqual(created_note.title, self.new_created_note['title'])
        # self.assertEqual(created_note.text, self.new_created_note['text'])
        # self.assertEqual(created_note.author, self.author)

    @unittest.skip(reason='')
    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(URL_NOTES_ADD, data=self.new_created_note)
        self.assertEqual(notes, set(Note.objects.all()))

    @unittest.skip(reason='')
    def test_cant_create_note_with_duplicate_slug(self):
        notes = set(Note.objects.all())
        self.new_created_note['slug'] = self.note.slug
        self.author_client.post(URL_NOTES_ADD, data=self.new_created_note)
        self.assertEqual(set(Note.objects.all()), notes)

    @unittest.skip(reason='')
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

    @unittest.skip(reason='')
    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=self.new_created_note
        ).status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    @unittest.skip(reason='')
    def test_author_can_delete_note(self):
        start_notes_count = Note.objects.count()
        self.author_client.delete(URL_NOTES_DELETE)
        self.assertEqual(start_notes_count, Note.objects.count() + 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    @unittest.skip(reason='')
    def test_user_cant_delete_note_of_another_user(self):
        start_notes_count = Note.objects.count()
        self.assertEqual(
            self.reader_client.delete(
                URL_NOTES_DELETE).status_code, HTTPStatus.NOT_FOUND
        )
        self.assertEqual(start_notes_count, Note.objects.count())
        self.assertIsInstance(self.note, Note)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
