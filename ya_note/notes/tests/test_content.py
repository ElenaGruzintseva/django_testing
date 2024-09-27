from notes.forms import NoteForm
from .conftest import (
    TestBase, URL_NOTES_LIST, URL_NOTES_ADD,
    URL_NOTES_EDIT, URL_NOTES_ADD, URL_NOTES_EDIT
)


class TestContent(TestBase):

    def test_notes_list_display(self):
        self.assertIn(self.note, self.author_client.get(URL_NOTES_LIST)
                      .context['object_list'])

    def test_note_not_in_list_for_another_user(self):
        self.assertNotIn(self.note, self.reader_client.get(URL_NOTES_LIST)
                         .context['object_list'])

    def test_create_edit_page(self):
        for url in (URL_NOTES_ADD, URL_NOTES_EDIT):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
