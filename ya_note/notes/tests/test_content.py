from notes.forms import NoteForm
from .conftest import (
    TestBase, URL_NOTES_LIST, URL_NOTES_ADD,
    URL_NOTES_EDIT, URL_NOTES_ADD, URL_NOTES_EDIT
)


class TestContent(TestBase):

    def test_notes_list_display(self):
        notes = self.author_client.get(URL_NOTES_LIST).context[
            'object_list']
        self.assertIn(self.note, notes)
        note = notes.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_note_not_in_list_for_another_user(self):
        self.assertNotIn(self.note, self.reader_client.get(URL_NOTES_LIST)
                         .context['object_list'])

    def test_create_edit_page(self):
        for url in (URL_NOTES_ADD, URL_NOTES_EDIT):
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
