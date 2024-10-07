from notes.forms import NoteForm
from .conftest import (
    TestBase, URL_NOTES_LIST, URL_NOTES_ADD,
    URL_NOTES_EDIT, URL_NOTES_ADD, URL_NOTES_EDIT
)


class TestContent(TestBase):

    def test_notes_list_display(self):
        list_notes = self.author_client.get(URL_NOTES_LIST).context[
            'object_list']
        self.assertIn(self.note, list_notes)
        note_in_list = list_notes.get(id=self.note.id)
        self.assertEqual(note_in_list.title, self.note.title)
        self.assertEqual(note_in_list.text, self.note.text)
        self.assertEqual(note_in_list.slug, self.note.slug)
        self.assertEqual(note_in_list.author, self.note.author)

    def test_note_not_in_list_for_another_user(self):
        self.assertNotIn(self.note, self.reader_client.get(URL_NOTES_LIST)
                         .context['object_list'])

    def test_create_edit_page(self):
        for url in (URL_NOTES_ADD, URL_NOTES_EDIT):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
