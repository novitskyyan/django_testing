from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTES_LIST_URL = 'notes:list'
NOTES_ADD_URL = 'notes:add'
NOTES_HOME_URL = 'notes:home'
NOTES_DETAIL_URL = 'notes:detail'
NOTES_SUCCESS_URL = 'notes:success'
NOTES_DELETE_URL = 'notes:delete'
NOTES_EDIT_URL = 'notes:edit'
AUTH_USERS_LOGIN_URL = 'users:login'
AUTH_USERS_LOGOUT_URL = 'users:logout'
AUTH_USERS_SIGNUP_URL = 'users:signup'

LOGIN_URL = (reverse('users:login'))


class BaseTestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username="Автор")
        cls.reader = User.objects.create(username="Читатель")
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок 1',
            text='Текст заметки',
            slug='note_1',
            author=cls.author
        )
        cls.note_slug = cls.note.slug
        cls.request_data = {
            'title': 'Заголовок 2',
            'text': 'Текст',
            'slug': 'note_2',
            'author': cls.author
        }
        cls.notes_for_edit = reverse('notes:edit', args=(cls.note_slug,))
