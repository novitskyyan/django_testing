from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

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
        cls.author_client.force_login(cls.author)
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок 1',
            text='Текст заметки',
            slug='note_1',
            author=cls.author
        )

    def test_notes_list(self):
        with self.subTest(user=self.author):
            url = reverse('notes:list')
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['object_list'].count(), 1
            )
            self.assertIn(self.note, response.context['object_list'])

    def test_reader_not_list(self):
        with self.subTest(user=self.author):
            url = reverse('notes:list')
            response = self.reader_client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context['object_list'].count(), 0
            )
            self.assertNotIn(self.note, response.context['object_list'])

    def test_add_page_has_forms(self):
        url = reverse('notes:add')
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)


    def test_edit_page_has_forms(self):
        url = reverse('notes:edit', args=[self.note.slug])
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)









