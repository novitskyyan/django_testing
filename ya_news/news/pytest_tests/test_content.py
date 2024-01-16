import pytest
from django.conf import settings

from news.forms import CommentForm
from .conftest import pytestmark


@pytestmark
@pytest.mark.usefixtures('news_on_home_page')
def test_news_count_on_homepage(admin_client, news_home):
    response = admin_client.get(news_home)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_home):
    response = client.get(news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news_detail_with_comments):
    response = client.get(news_detail_with_comments)
    news = response.context['news']
    comments_list = news.comment_set.all()
    all_dates = [comment.created for comment in comments_list]
    assert all_dates == sorted(all_dates)


def test_anonymous_client_has_no_form(client, news, news_detail):
    response = client.get(news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news, news_detail):
    response = author_client.get(news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
