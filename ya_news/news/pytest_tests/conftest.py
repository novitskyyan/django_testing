from datetime import datetime, timedelta

import pytest
from django.conf import settings

from news.forms import BAD_WORDS
from news.models import Comment, News


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
def form_data():
    return {
        'text': 'Комментарий пользователя'
    }


@pytest.fixture
def new_form_data():
    return {
        'text': 'Новый комментарий пользователя'
    }


@pytest.fixture
def news_on_home_page():
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        news = News(title=f'Новость {index}', text='Просто текст.')
        news.save()


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
def bad_comment_data():
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
