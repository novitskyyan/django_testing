from http import HTTPStatus

from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup', 'news:detail')
)
@pytest.mark.django_db
def test_pages_available_for_anonymous_user(client, news, name):
    if name == 'news:detail':
        url = reverse(name, args=(news.pk,))
    else:
        url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
@pytest.mark.django_db
def test_edit_and_delete_comment_for_different_users(
        parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_comment_anonymous_cant_edit_or_delete(
        client, comment, name
):
    url = reverse(name, args=(comment.pk,))
    response = client.get(url)
    url_login = reverse('users:login')
    expected_url = f'{url_login}?next={url}'
    assertRedirects(response, expected_url)
