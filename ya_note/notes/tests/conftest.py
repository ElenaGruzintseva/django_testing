from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

CREATE_NOTES_COUNT = 10

User = get_user_model()


class TestBase(TestCase):

    @classmethod
    def setUpTestData(
        cls,
        generate_note=False,
        generate_note_list=False
    ):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        if generate_note:
            cls.note = Note.objects.create(
                title='Заметка 1',
                text='Просто текст',
                author=cls.author,
                slug='Zametka-1'
            )

        if generate_note_list:
            cls.notes = Note.objects.bulk_create(
                Note(
                    title=f'Заметка {index}',
                    text='Просто текст.',
                    author=cls.author,
                    slug=f'Zametka-{index}'
                )for index in range(CREATE_NOTES_COUNT)
            )
