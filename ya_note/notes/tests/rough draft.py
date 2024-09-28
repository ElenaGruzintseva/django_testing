from http import HTTPStatus
import unittest
from pytils.translit import slugify
from notes.models import Note
from .conftest import (
    TestBase, URL_NOTES_ADD, URL_NOTES_SUCCESS,
    URL_NOTES_EDIT, URL_NOTES_DELETE
)


class CreatedNote(TestBase):

    def method_created_note(self, field_data):
        note = Note.objects.get()
        db_data = (note.title, note.text, note.slug, note.author)
        for name, sent_value, db_value in zip(
            FIELD_NAMES, field_data, db_data
        ):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(sent_value, db_value)

    def equal(self, expected_count):
        notes_count = Note.objects.count()
        self.assertEqual(expected_count, notes_count)


class TestCreateNote(CreatedNote):

    def test_user_can_create_note(self):
        expected_count = Note.objects.count() + 1
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.form_data),
            URL_NOTES_SUCCESS)
        super().equal(expected_count)
        super().method_created_note(self.field_data)
