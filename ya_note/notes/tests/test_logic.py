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
                URL_NOTES_ADD, data=self.someones_note), URL_NOTES_SUCCESS
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.someones_note['title'])
        self.assertEqual(note.text, self.someones_note['text'])
        self.assertEqual(note.slug, self.someones_note['slug'])
        self.assertEqual(note.author, self.author)

    def test_user_can_create_note_without_slug(self):
        notes = set(Note.objects.all())
        self.someones_note.pop('slug')
        self.assertRedirects(
            self.author_client.post(URL_NOTES_ADD, data=self.someones_note),
            URL_NOTES_SUCCESS)
        notes = set(Note.objects.all()).difference(notes)
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, slugify(self.someones_note['title']))
        self.assertEqual(note.title, self.someones_note['title'])
        self.assertEqual(note.text, self.someones_note['text'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        initial_notes = set(Note.objects.all())
        self.client.post(URL_NOTES_ADD, data=self.someones_note)
        final_notes = set(Note.objects.all())
        assert initial_notes == final_notes
        try:
            comment = Note.objects.get(text=self.someones_note['text'],
                                       title=self.someones_note['title'],
                                       slug=self.someones_note['slug'],
                                       author=self.author)
            assert comment.author is None
        except Note.DoesNotExist:
            pass

    def test_cant_create_note_with_duplicate_slug(self):
        initial_notes = list(Note.objects.all())
        self.someones_note['slug'] = self.note.slug
        self.author_client.post(URL_NOTES_ADD, data=self.someones_note)
        final_notes = list(Note.objects.all())
        assert initial_notes == final_notes
        try:
            comment = Note.objects.get(text=self.someones_note['text'],
                                       title=self.someones_note['title'],
                                       slug=self.someones_note['slug'],
                                       author=self.author)
            assert comment.author is None
        except Note.DoesNotExist:
            pass

    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                URL_NOTES_EDIT, data=self.someones_note
            ).status_code, HTTPStatus.FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.someones_note['title'])
        self.assertEqual(note.text, self.someones_note['text'])
        self.assertEqual(note.slug, self.someones_note['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            URL_NOTES_EDIT, data=self.someones_note
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
        original_note = Note.objects.get(id=self.note.id)
        original_title = original_note.title
        original_text = original_note.text
        original_author = original_note.author
        original_slug = original_note.slug
        response = self.reader_client.delete(URL_NOTES_DELETE, data=self.note)
        assert response.status_code == HTTPStatus.NOT_FOUND
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, original_title)
        self.assertEqual(note.text, original_text)
        self.assertEqual(note.author, original_author)
        self.assertEqual(note.slug, original_slug)
