from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(
            username='Автор'
        )
        cls.reader = User.objects.create(
            username='Читатель'
        )
        cls.author_client = Client()
        cls.reader_client = Client()
        cls.note = Note.objects.create(
            title='Заголовок 1',
            text='Текст заметки',
            slug='note_1',
            author=cls.author
        )
        cls.request_data = {
            'title': 'Заголовок 2',
            'text': 'Текст',
            'slug': 'note_2',
            'author': cls.author
        }

    def test_authenticated_user_add_note(self):
        self.author_client.force_login(self.author)
        url = reverse('notes:add')
        response = self.author_client.post(url, data=self.request_data)
        self.assertRedirects(response, reverse('notes:success'))

    def test_anonymous_user_cant_create_note(self):
        url = reverse('notes:add')
        response = self.client.post(url, data=self.request_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_url)

    def test_no_create_note_with_same_slug(self):
        self.request_data['slug'] = self.note.slug
        self.author_client.force_login(self.author)
        url = reverse('notes:add')
        response = self.author_client.post(url, data=self.request_data)
        self.assertFormError(response, 'form', 'slug',
                             errors=self.note.slug + WARNING)

    def test_generate_slug(self):
        self.author_client.force_login(self.author)
        del self.request_data['slug']
        url = reverse('notes:add')
        response = self.author_client.post(url, data=self.request_data)
        self.assertRedirects(response, reverse('notes:success'))
        note = Note.objects.last()
        expected_slug = slugify(self.request_data['title'])
        self.assertEqual(note.slug, expected_slug)

    def test_edit_post_by_user(self):
        data = {
            'title': 'Новый измененный заголовок',
            'text': 'Новый измененный текст',
        }
        self.author_client.force_login(self.author)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.author_client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        note = Note.objects.first()
        self.assertEqual(note.text, data['text'])

    def test_reader_not_edit_any_post(self):
        data = {
            'title': 'Новый измененный заголовок',
            'text': 'Новый измененный текст',
        }
        self.reader_client.force_login(self.reader)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.reader_client.post(url, data=data)
        self.assertEqual(response.status_code, 404)
