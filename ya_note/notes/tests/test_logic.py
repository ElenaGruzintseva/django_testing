from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)


class TestLogic(TestBase):

    def test_user_can_create_note(self):
        notes = set(Note.objects.all())
        self.assertRedirects(
            self.author_client.post(
                URL_NOTES_ADD, data=self.field_form), URL_NOTES_SUCCESS
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.field_form['title'])
        self.assertEqual(note.text, self.field_form['text'])
        self.assertEqual(note.slug, self.field_form['slug'])
        self.assertEqual(note.author, self.author)

    def test_user_can_create_note_without_slug(self):
        notes = set(Note.objects.all())
        self.field_form.pop('slug')
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.field_form),
            URL_NOTES_SUCCESS)
        notes = set(Note.objects.all()).difference(notes)
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, slugify(self.field_form['title']))
        self.assertEqual(note.title, self.field_form['title'])
        self.assertEqual(note.text, self.field_form['text'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        initial_notes = set(Note.objects.all())
        self.client.post(URL_NOTES_ADD, data={'text': self.field_form})
        self.assertEqual(initial_notes, set(Note.objects.all()))

    def test_cant_create_note_with_duplicate_slug(self):
        initial_notes = set(Note.objects.all())
        self.field_form['slug'] = self.note.slug
        self.author_client.post(URL_NOTES_ADD, data={'text': self.field_form})
        self.assertEqual(initial_notes, set(Note.objects.all()))

    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                URL_NOTES_EDIT, data=self.field_form
            ).status_code, HTTPStatus.FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.field_form['title'])
        self.assertEqual(note.text, self.field_form['text'])
        self.assertEqual(note.slug, self.field_form['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=self.field_form
        ).status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    def test_author_can_delete_note(self):
        expected_count = Note.objects.count() - 1
        self.author_client.delete(URL_NOTES_DELETE)
        self.assertEqual(expected_count, Note.objects.count())
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cant_delete_note_of_another_user(self):
        initial_notes = set(Note.objects.all())
        response = self.reader_client.delete(URL_NOTES_DELETE, data=self.note)
        assert response.status_code == HTTPStatus.NOT_FOUND
        final_notes = set(Note.objects.all())
        self.assertEqual(initial_notes, final_notes)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(note_from_db.author, self.note.author)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.slug, self.note.slug)
