import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


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


NEWS_HOME = reverse('news:home')
NEWS_HOME_URL = 'news:home'
NEWS_DETAIL_URL = 'news:detail'
NEWS_DELETE_URL = 'news:delete'
NEWS_EDIT_URL = 'news:edit'
USERS_LOGIN_URL = 'users:login'
USERS_LOGOUT_URL = 'users:logout'
USERS_SIGNUP_URL = 'users:signup'

AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
ADMIN_CLIENT = pytest.lazy_fixture('admin_client')
CLIENT = pytest.lazy_fixture('client')
