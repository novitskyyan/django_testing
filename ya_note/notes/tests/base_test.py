from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_HOME_URL = reverse('notes:home')
NOTES_SUCCESS_URL = reverse('notes:success')
AUTH_USERS_LOGIN_URL = reverse('users:login')
AUTH_USERS_LOGOUT_URL = reverse('users:logout')
AUTH_USERS_SIGNUP_URL = reverse('users:signup')
NOTES_EDIT_URL = 'notes:edit'
NOTES_DETAIL_URL = 'notes:detail'
NOTES_DELETE_URL = 'notes:delete'

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
        cls.notes_for_detail = reverse('notes:detail', args=(cls.note_slug,))
        cls.notes_for_delete = reverse('notes:delete', args=(cls.note_slug,))
