from django.urls import reverse
from rest_framework import status
from tests.fixtures import FixtureMixin


class TestBegin(FixtureMixin):

    def test_not_avalilable_for_anonymous(self):
        for url in [self.users_url, self.users_id_url]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_401_UNAUTHORIZED
                )

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
    
    def test_available_method_for_users(self):
        methods = (
            ('get', status.HTTP_200_OK, {}),
            ('post', status.HTTP_201_CREATED, self.data_for_register),
            ('put', status.HTTP_405_METHOD_NOT_ALLOWED, self.data_for_register),
            ('patch', status.HTTP_405_METHOD_NOT_ALLOWED, self.data_for_register),
        )
        for method, code, data in methods:
            with self.subTest(method=method, code=code):
                response = eval(
                    f'self.client_with_token.{method}(self.users_url, data={data})'
                )
                self.assertEqual(response.status_code, code)

    def test_available_method_for_users_id(self):
        methods = (
            ('get', status.HTTP_200_OK, {}),
            ('post', status.HTTP_405_METHOD_NOT_ALLOWED, self.data_for_register),
            ('put', status.HTTP_405_METHOD_NOT_ALLOWED, self.data_for_register),
            ('patch', status.HTTP_405_METHOD_NOT_ALLOWED, self.data_for_register),
        )
        for method, code, data in methods:
            with self.subTest(method=method, code=code):
                response = getattr(
                    self.client_with_token,
                    method
                )(self.users_id_url, data=data)
                self.assertEqual(response.status_code, code)

    def test_pagination(self):
        response = self.client_with_token.get(self.users_url)