from django.urls import reverse

NEWS_HOME_URL = 'news:home'
NEWS_DETAIL_URL = 'news:detail'
NEWS_DELETE_URL = 'news:delete'
NEWS_EDIT_URL = 'news:edit'
USERS_LOGIN_URL = reverse('users:login')
USERS_LOGOUT_URL = reverse('users:logout')
USERS_SIGNUP_URL = reverse('users:signup')
