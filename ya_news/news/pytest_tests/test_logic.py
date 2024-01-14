from http import HTTPStatus

from django.forms import model_to_dict
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import WARNING, BAD_WORDS
from news.models import Comment
from news.pytest_tests.global_constants import NEWS_DETAIL_URL, \
    USERS_LOGIN_URL

form_data = {
    'text': 'Комментарий пользователя',
    'author': 'Автор',
    'news': 'Новость'
}

new_form_data = {
    'text': 'Новый комментарий пользователя',
}

bad_comment_data = {
    'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'
}


def test_user_can_create_comment(author_client, author, news, news_detail):
    assert Comment.objects.count() == 0
    response = author_client.post(news_detail, data=form_data)
    assertRedirects(response, f'{news_detail}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']


def test_anonymous_user_cant_create_comment(client, news, news_detail):
    response = client.post(news_detail, data=form_data)
    url_login = reverse(USERS_LOGIN_URL)
    expected_url = f'{url_login}?next={news_detail}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment, news_edit):
    comment_before_refresh = model_to_dict(comment, fields='text')
    original_comment_without_text = model_to_dict(comment, exclude='text')
    author_client.post(news_edit, data=new_form_data)
    comment.refresh_from_db()
    new_comment_without_text = model_to_dict(comment, exclude='text')
    new_comment_after_refresh = model_to_dict(comment, fields='text')
    assert new_comment_after_refresh != comment_before_refresh
    assert original_comment_without_text == new_comment_without_text


def test_user_cant_edit_comment_of_another_user(
        admin_client, comment, news_edit
):
    comment_before_refresh = model_to_dict(comment)
    response = admin_client.post(news_edit, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert model_to_dict(comment) == comment_before_refresh


def test_user_cant_delete_comment_of_another_user(
        admin_client, comment, news_delete
):
    response = admin_client.delete(news_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_delete_comment(author_client, comment, news_delete):
    author_client.delete(news_delete)
    assert Comment.objects.count() == 0


def test_forbiddance_of_bad_words_on_comment(
        author_client, news
):
    url = reverse(NEWS_DETAIL_URL, args=(news.pk,))
    response = author_client.post(url, data=bad_comment_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
