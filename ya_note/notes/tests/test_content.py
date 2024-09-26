from http import HTTPStatus

from notes.forms import NoteForm
from notes.models import Note
from .conftest import TestBase
from .constants_urls import (
    URL_NOTES_LIST, URL_NOTES_ADD, URL_NOTES_EDIT,
    URL_NOTES_ADD, URL_NOTES_EDIT
)


class TestContent(TestBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData(generate_note=True)

    def test_notes_list_display(self):
        self.assertIn(self.note, self.author_client.get(URL_NOTES_LIST)
                      .context['object_list'])
        notes = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, notes.title)
        self.assertEqual(self.note.text, notes.text)
        self.assertEqual(self.note.author, notes.author)
        self.assertEqual(self.note.slug, notes.slug)

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(URL_NOTES_LIST)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_create_edit_page(self):
        for url in (URL_NOTES_ADD, URL_NOTES_EDIT):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
