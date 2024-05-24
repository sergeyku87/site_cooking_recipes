
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token


class FixtureMixin(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            username='Bob',
            email='bob@bob.com',
            password=make_password('fhfyr8756SDFxff8')
        )
        cls.admin_user = get_user_model().objects.create(
            username='Admin',
            email='admin@admin.com',
            password=make_password('uthdkFFDD87shk'),
            is_staff=True,
            is_superuser=True,
        )
        cls.simple_user = get_user_model().objects.create(
            username='Simple',
            email='simple@simple.com',
            password=make_password('irirhdhur&&66ydhDDD'),
        )
        cls.admin_client = APIClient()
        cls.client_with_token = APIClient()
        cls.client_without_token = APIClient()

        cls.admin_client.force_login(cls.admin_user)
        cls.client_with_token.force_login(cls.user)
        cls.client_without_token.force_login(cls.simple_user)

        cls.client_with_token.post(
            reverse('login'),
            data={
                'email': 'bob@bob.com',
                'password': 'fhfyr8756SDFxff8'
            }
        )
        token = Token.objects.get(user__username='Bob')

        cls.client_with_token.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key
        )

        cls.users_url = reverse('user-list')
        cls.users_id_url = reverse('user-detail', args=(1,))
        cls.user_me_url = reverse('user-me')
        cls.user_me_avatar_url = reverse('user-avatar')
        cls.login_url = reverse('login')
        cls.logout_url = reverse('logout')
        cls.data_for_register = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Иванов",
            "password": "Qwerty123"
        }

    def get_token(self, username, email, password):
        self.client.post(
            self.login,
            data={
                'email': email,
                'password': password,
            }
        )
        token = Token.objects.get(user__username=username)
        return token.key

    @classmethod
    def tearDownClass(self):
        ...


