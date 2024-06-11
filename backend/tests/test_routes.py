from django.urls import reverse
from rest_framework import status
from tests.fixtures import FixtureMixin


class TestBegin(FixtureMixin):
    def test_available_for_auth_client(self):
        for url in [self.users_url, self.users_id_url]:
            with self.subTest(url=url):
                response = self.client_without_token.get(self.users_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_for_client_with_token(self):
        for url in [self.users_url, self.users_id_url]:
            with self.subTest(url=url):
                response = self.client_with_token.get(self.users_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
