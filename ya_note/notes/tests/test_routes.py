from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from notes.tests.base_test import BaseTestContent, AUTH_USERS_LOGIN_URL, \
    AUTH_USERS_LOGOUT_URL, AUTH_USERS_SIGNUP_URL, NOTES_HOME_URL, \
    NOTES_LIST_URL, NOTES_SUCCESS_URL, NOTES_ADD_URL, NOTES_DETAIL_URL, \
    NOTES_DELETE_URL, NOTES_EDIT_URL, LOGIN_URL

User = get_user_model()


class TestRoutes(BaseTestContent):

    def test_pages_available_for_users(self):
        urls = (
            (AUTH_USERS_LOGIN_URL, self.client, HTTPStatus.OK),
            (AUTH_USERS_LOGOUT_URL, self.client, HTTPStatus.OK),
            (AUTH_USERS_SIGNUP_URL, self.client, HTTPStatus.OK),
            (NOTES_HOME_URL, self.client, HTTPStatus.OK),
            (NOTES_LIST_URL, self.author_client, HTTPStatus.OK),
            (NOTES_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (NOTES_ADD_URL, self.author_client, HTTPStatus.OK),
        )

        for name, client, status in urls:
            with self.subTest(name=name, client=client, status=status):
                response = client.get(name)
                self.assertEqual(response.status_code, status)

    def test_note_available_or_not_for_users(self):
        users = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        url_names = (NOTES_DETAIL_URL,
                     NOTES_DELETE_URL,
                     NOTES_EDIT_URL
                     )
        for user, status in users:
            client = Client()
            client.force_login(user)
            for url_name in url_names:
                with self.subTest(user=user, url_name=url_name):
                    url = reverse(url_name, args=(self.note.slug,))
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        urls = (
            NOTES_LIST_URL,
            NOTES_SUCCESS_URL,
            NOTES_ADD_URL,
            self.notes_for_detail,
            self.notes_for_edit,
            self.notes_for_delete,
        )

        for name in urls:
            with self.subTest(name=name):
                redirect_url = f'{LOGIN_URL}?next={name}'
                response = self.client.get(name)
                self.assertRedirects(response, redirect_url)
