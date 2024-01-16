from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse

from news.models import Comment, News
from news.pytest_tests.global_constants import USERS_LOGIN_URL

pytestmark = pytest.mark.django_db


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture(scope='function')
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text="Текст комментария"
    )
    return comment


@pytest.fixture
def news_on_home_page():
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        news = News(title=f'Новость {index}', text='Просто текст.')
        news.save()


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_with_comments(news, author):
    comments = [
        Comment(news=news,
                author=author,
                text=f"Текст комментария {index}"
                )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    Comment.objects.bulk_create(comments)
    return news


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f"Новость {index}",
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_edit(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def news_delete(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def news_home():
    return reverse('news:home')


@pytest.fixture
def users_logout():
    return reverse('users:logout')


@pytest.fixture
def users_login():
    return reverse('users:login')


@pytest.fixture
def users_signup():
    return reverse('users:signup')


@pytest.fixture
def news_detail_with_comments(news_with_comments):
    return reverse('news:detail', args=(news_with_comments.pk,))


@pytest.fixture
def expected_url_for_login(news_detail):
    return f'{USERS_LOGIN_URL}?next={news_detail}'
