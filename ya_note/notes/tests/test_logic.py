from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)


FORM_DATA_NOTE = {
    'title': 'Заметка 2',
    'text': 'Просто текст2',
    'slug': 'Zametka-2'
}

FORM_DATA_NO_SLUG = {
    'title': 'Интересность',
    'text': 'Просто текст',
    'slug': '',
}

FORM_DATA_DUPLICATE_SLUG = {
    'title': 'Заметка 1',
    'text': 'Просто текст',
    'slug': 'Zametka-1'
}

# import unittest
# @unittest.skip(reason='Пока пропускаем.')

class TestLogic(TestBase):

    def test_user_can_create_note(self):
        notes = set(Note.objects.all())
        self.assertRedirects(self.author_client.post(
            URL_NOTES_ADD, data=FORM_DATA_NOTE), URL_NOTES_SUCCESS
        )
        difference = set(Note.objects.all()) - notes
        self.assertEqual(len(difference), 1)
        new_note = difference.pop()
        self.assertEqual(new_note.title, FORM_DATA_NOTE['title'])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, FORM_DATA_NOTE['slug'])
        self.assertEqual(new_note.text, FORM_DATA_NOTE['text'])

    def test_anonymous_user_cant_create_note(self):
        notes = set(Note.objects.all())
        self.client.post(URL_NOTES_ADD, data=FORM_DATA_NOTE)
        self.assertEqual(notes, set(Note.objects.all()))

    def test_cant_create_note_with_duplicate_slug(self):
        notes = set(Note.objects.all())
        self.author_client.post(
            URL_NOTES_ADD,
            data=FORM_DATA_DUPLICATE_SLUG
        )
        self.assertEqual(set(Note.objects.all()), notes)

    def test_user_can_create_note_without_slug(self):
        Note.objects.all().delete()
        FORM_DATA_NO_SLUG.pop('slug')
        response = self.author_client.post(
            URL_NOTES_ADD, data=FORM_DATA_NO_SLUG
        )
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        created_note = Note.objects.get(title=FORM_DATA_NO_SLUG['title'])
        self.assertEqual(
            created_note.slug, slugify(FORM_DATA_NO_SLUG['title'])
        )
        self.assertEqual(created_note.title, FORM_DATA_NO_SLUG['title'])
        self.assertEqual(created_note.text, FORM_DATA_NO_SLUG['text'])
        self.assertEqual(created_note.author, self.author)

    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                URL_NOTES_EDIT, data=FORM_DATA_NOTE
            ).status_code, HTTPStatus.FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, FORM_DATA_NOTE['title'])
        self.assertEqual(note.text, FORM_DATA_NOTE['text'])
        self.assertEqual(note.slug, FORM_DATA_NOTE['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=FORM_DATA_NOTE
        ).status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    def test_author_can_delete_note(self):
        start_notes_count = Note.objects.count()
        self.author_client.delete(URL_NOTES_DELETE)
        self.assertEqual(start_notes_count, Note.objects.count() + 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

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
