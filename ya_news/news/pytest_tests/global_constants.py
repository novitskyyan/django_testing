import pytest

pytestmark = pytest.mark.django_db

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
