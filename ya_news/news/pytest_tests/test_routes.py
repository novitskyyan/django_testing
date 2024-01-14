from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from news.pytest_tests.global_constants import (
    NEWS_DETAIL_URL,
    USERS_LOGIN_URL,
    NEWS_DELETE_URL, NEWS_EDIT_URL,
    NEWS_HOME_URL,
    USERS_SIGNUP_URL,
    USERS_LOGOUT_URL
)

AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
ADMIN_CLIENT = pytest.lazy_fixture('admin_client')
CLIENT = pytest.lazy_fixture('client')


@pytest.mark.parametrize(
    'name_url, parametrized_client, expected_status',
    (
            (NEWS_HOME_URL, ADMIN_CLIENT, HTTPStatus.OK),
            (USERS_LOGIN_URL, ADMIN_CLIENT, HTTPStatus.OK),
            (USERS_LOGOUT_URL, ADMIN_CLIENT, HTTPStatus.OK),
            (USERS_SIGNUP_URL, ADMIN_CLIENT, HTTPStatus.OK),
            (NEWS_DETAIL_URL, ADMIN_CLIENT, HTTPStatus.OK),
            (NEWS_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
            (NEWS_DELETE_URL, ADMIN_CLIENT, HTTPStatus.NOT_FOUND),
            (NEWS_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
            (NEWS_EDIT_URL, ADMIN_CLIENT, HTTPStatus.NOT_FOUND)
    ))
def test_pages_available_for_anonymous_user(
        parametrized_client,
        news,
        news_detail,
        news_edit,
        news_delete,
        comment,
        name_url,
        expected_status
):
    if name_url == NEWS_DETAIL_URL:
        url = news_detail
    elif name_url == NEWS_DELETE_URL:
        url = news_delete
    elif name_url == NEWS_EDIT_URL:
        url = news_edit
    else:
        url = reverse(name_url)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (NEWS_DELETE_URL, NEWS_EDIT_URL),
)
def test_comment_anonymous_cant_edit_or_delete(
        client, comment, name
):
    url = reverse(name, args=(comment.pk,))
    response = client.get(url)
    url_login = reverse(USERS_LOGIN_URL)
    expected_url = f'{url_login}?next={url}'
    assertRedirects(response, expected_url)
