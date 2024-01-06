from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.forms import WARNING
from news.models import Comment


@pytest.mark.django_db
def test_user_can_create_comment(author_client, author, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    assertRedirects(response, '/auth/login/?next=%2Fnews%2F1%2F')
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, new_form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    author_client.post(url, data=new_form_data)
    comment.refresh_from_db()
    assert comment.text == new_form_data['text']


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
        admin_client, new_form_data, comment
):
    url = reverse('news:edit', args=(comment.pk,))
    response = admin_client.post(url, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != new_form_data['text']


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
        admin_client, comment
):
    url = reverse('news:delete', args=(comment.pk,))
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, comment):
    url = reverse('news:delete', args=(comment.pk,))
    author_client.delete(url)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_forbiddance_of_bad_words_on_comment(
        author_client, news, bad_comment_data
):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=bad_comment_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
