from http import HTTPStatus

from django.contrib.auth import get_user_model

from .base_test import BaseTestContent, NOTES_LIST_URL, NOTES_ADD_URL
from ..forms import NoteForm

User = get_user_model()


class TestContent(BaseTestContent):

    def test_notes_list(self):
        with self.subTest(user=self.author):
            response = self.author_client.get(NOTES_LIST_URL)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.context['object_list'].count(), 1
            )
            self.assertIn(self.note, response.context['object_list'])

    def test_reader_not_list(self):
        response = self.reader_client.get(NOTES_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context['object_list'].count(), 0
        )
        self.assertNotIn(self.note, response.context['object_list'])

    def test_add_page_has_forms(self):
        response = self.author_client.get(NOTES_ADD_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('form', response.context)

    def test_edit_page_has_forms(self):
        response = self.author_client.get(self.notes_for_edit)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
