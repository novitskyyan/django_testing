from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .base_test import BaseTestContent, AUTH_USERS_LOGIN_URL
from .base_test import NOTES_ADD_URL, NOTES_SUCCESS_URL

User = get_user_model()


class TestLogic(BaseTestContent):

    def test_authenticated_user_add_note(self):
        count_of_notes_before = Note.objects.count()
        url = reverse(NOTES_ADD_URL)
        response = self.author_client.post(url, data=self.request_data)
        self.assertRedirects(response, reverse(NOTES_SUCCESS_URL))
        count_of_notes_after = Note.objects.count()
        self.assertEqual(count_of_notes_before, count_of_notes_after - 1)

    def test_anonymous_user_cant_create_note(self):
        count_of_notes_before = Note.objects.count()
        url = reverse(NOTES_ADD_URL)
        response = self.client.post(url, data=self.request_data)
        login_url = reverse(AUTH_USERS_LOGIN_URL)
        expected_url = f'{login_url}?next={url}'
        count_of_notes_after = Note.objects.count()
        self.assertRedirects(response, expected_url)
        self.assertEqual(count_of_notes_before, count_of_notes_after)

    def test_no_create_note_with_same_slug(self):
        count_of_notes_before = Note.objects.count()
        self.request_data['slug'] = self.note.slug
        self.author_client.force_login(self.author)
        url = reverse(NOTES_ADD_URL)
        response = self.author_client.post(url, data=self.request_data)
        count_of_notes_after = Note.objects.count()
        self.assertFormError(response, 'form', 'slug',
                             errors=self.note.slug + WARNING)
        self.assertEqual(count_of_notes_before, count_of_notes_after)

    def test_generate_slug(self):
        self.author_client.force_login(self.author)
        del self.request_data['slug']
        url = reverse(NOTES_ADD_URL)
        response = self.author_client.post(url, data=self.request_data)
        self.assertRedirects(response, reverse(NOTES_SUCCESS_URL))
        note = Note.objects.last()
        expected_slug = slugify(self.request_data['title'])
        self.assertEqual(note.slug, expected_slug)

    def test_edit_post_by_user(self):
        data = {
            'title': 'Новый измененный заголовок',
            'text': 'Новый измененный текст',
        }
        self.author_client.force_login(self.author)
        response = self.author_client.post(self.notes_for_edit, data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        note = Note.objects.first()
        self.assertEqual(note.text, data['text'])

    def test_reader_not_edit_any_post(self):
        data = {
            'title': 'Новый измененный заголовок',
            'text': 'Новый измененный текст',
        }
        self.reader_client.force_login(self.reader)
        response = self.reader_client.post(self.notes_for_edit, data=data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
