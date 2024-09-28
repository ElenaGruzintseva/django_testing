from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)


class CreatedNote(TestBase):

    def method_created_note(self, field_data):
        note = Note.objects.get(title=field_data['title'])
        data = dict(field_data)
        for key, value in data.items():
            with self.subTest(key=key, value=value):
                self.assertEqual(note.title, data['title'])
                self.assertEqual(note.text, data['text'])
                self.assertEqual(note.slug, data['slug'])
                self.assertEqual(note.author, self.author)

    def equal(self, expected_count):
        notes_count = Note.objects.count()
        self.assertEqual(expected_count, notes_count)


class TestLogic(CreatedNote):

    def test_user_can_create_note(self):
        expected_count = Note.objects.count() + 1
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.new_created_note),
            URL_NOTES_SUCCESS)
        super().equal(expected_count)
        super().method_created_note(self.new_created_note)

    def test_user_can_create_note_without_slug(self):
        expected_count = Note.objects.count() + 1
        self.new_created_note.pop('slug')
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.new_created_note),
            URL_NOTES_SUCCESS)
        super().equal(expected_count)
        new_created_note = Note.objects.get(
            title=self.new_created_note['title']
        )
        self.assertEqual(
            new_created_note.slug, slugify(self.new_created_note['title'])
        )

    def test_anonymous_user_cant_create_note(self):
        expected_count = Note.objects.count()
        self.client.post(URL_NOTES_ADD, data=self.new_created_note)
        super().equal(expected_count)

    def test_cant_create_note_with_duplicate_slug(self):
        expected_count = Note.objects.count()
        self.new_created_note['slug'] = self.note.slug
        self.author_client.post(URL_NOTES_ADD, data=self.new_created_note)
        super().equal(expected_count)

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

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=self.new_created_note
        ).status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    def test_author_can_delete_note(self):
        expected_count = Note.objects.count() - 1
        self.author_client.delete(URL_NOTES_DELETE)
        super().equal(expected_count)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cant_delete_note_of_another_user(self):
        expected_count = Note.objects.count()
        self.assertEqual(
            self.reader_client.delete(
                URL_NOTES_DELETE).status_code, HTTPStatus.NOT_FOUND
        )
        super().equal(expected_count)
        self.assertIsInstance(self.note, Note)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
