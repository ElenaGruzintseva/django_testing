from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'Zametka-1'
URL_HOME = reverse('notes:home')
URL_LOGIN = reverse('users:login')
URL_LOGOUT = reverse('users:logout')
URL_SIGNUP = reverse('users:signup')
URL_NOTES_LIST = reverse('notes:list')
URL_NOTES_ADD = reverse('notes:add')
URL_NOTES_SUCCESS = reverse('notes:success')
URL_NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
URL_NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))
URL_NOTES_DELETE = reverse('notes:delete', args=(SLUG,))


class TestBase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='Заметка 1',
            text='Просто текст',
            author=cls.author,
            slug='Zametka-1'
        )

        cls.new_created_note = {
            'title': 'Заметкаа',
            'text': 'Текст новой заметки',
            'slug': 'Zametkaa'
        }
