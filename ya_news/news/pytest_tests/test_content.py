import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm
from .global_constants import NEWS_HOME_URL, NEWS_DETAIL_URL, pytestmark


@pytestmark
@pytest.mark.usefixtures('news_on_home_page')
def test_news_count_on_homepage(admin_client):
    url = reverse(NEWS_HOME_URL)
    response = admin_client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client):
    url = reverse(NEWS_HOME_URL)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news_with_comments):
    url = reverse(NEWS_DETAIL_URL, args=(news_with_comments.pk,))
    response = client.get(url)
    news = response.context['news']
    comments_list = news.comment_set.all()
    all_dates = [comment.created for comment in comments_list]
    assert all_dates == sorted(all_dates)


def test_anonymous_client_has_no_form(client, news):
    url = reverse(NEWS_DETAIL_URL, args=(news.pk,))
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
