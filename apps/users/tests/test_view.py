from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from unittest.mock import patch


class RegisterViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("registration")
        self.request_data = {
            "username": "example",
            "email": "test12344@test.com",
            "name": "test12345",
            "password": "123",
            "password_confirm": "123",
        }
        self.response_keys = [
            "id",
            "username",
            "email",
            "name",
            "isAdmin",
            "is_verified",
        ]

    @patch("apps.users.views.send_otp_email")
    def test_user_registration(self, send_otp_email):
        response = self.client.post(self.url, self.request_data)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(
            list(response_data.keys()),
            ["id", "username", "email", "name", "isAdmin", "is_verified"],
        )
        self.assertEqual(response_data.get("email"), self.request_data.get("email"))
        self.assertEqual(
            response_data.get("username"), self.request_data.get("username")
        )
        self.assertEqual(response_data.get("name"), self.request_data.get("name"))
        self.assertEqual(
            response_data.get("is_verified"), User.objects.last().is_verified
        )
        self.assertEqual(response_data.get("id"), User.objects.last().id)

        send_otp_email.delay.assert_called_once_with(self.request_data.get("email"))

    def test_user_registration_without_data(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(list(response.data.keys()), list(self.request_data.keys()))

    def test_user_with_existing_username(self):
        self._test_user_with_existing_attributes("username")

    def test_user_with_existing_email(self):
        self._test_user_with_existing_attributes("email")

    def _test_user_with_existing_attributes(self, attribute_name: str):
        user = User.objects.create()
        self.request_data[attribute_name] = getattr(user, attribute_name)
        response = self.client.post(self.url, self.request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#
class LoginViewTestCase(APITestCase):
    EMAIL_KEY = "email"
    PASSWORD_KEY = "password"

    def setUp(self) -> None:
        self.url = reverse("login")
        self.user = User.objects.create(
            email="test1234@gmail.com", password=make_password("test1234")
        )
        self.login_data = self._generate_login_data(self.user.email, "test1234")

    def test_user_login(self):
        response = self.client.post(
            self.url, data=self._generate_login_data("test1234@gmail.com", "test1234")
        )
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response_data.keys()), ["refresh", "access"])
        self.assertIsInstance(response_data.get("refresh"), str)
        self.assertIsInstance(response_data.get("access"), str)

    def test_user_login_without_login_data(self):
        response = self.client.post(self.url)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertListEqual(
            list(response_data.keys()), [self.EMAIL_KEY, self.PASSWORD_KEY]
        )

    def test_user_login_with_invalid_email(self):
        response = self.client.post(
            self.url,
            data=self._generate_login_data("inccorectmail@gmail.com", "test1234"),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_incorrect_password(self):
        response = self.client.post(
            self.url, self._generate_login_data(self.user.email, "incorrectPass")
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def _generate_login_data(self, email: str, password: str) -> dict:
        return {self.EMAIL_KEY: email, self.PASSWORD_KEY: password}


class TokenRefreshViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("token_refresh")
        self.login_url = reverse("login")
        self.user = User.objects.create(
            email="test1234@gmail.com", password=make_password("test1234")
        )
        self.refresh_token = RefreshToken.for_user(self.user)

    def test_refresh_token_retrieval(self):
        response = self.client.post(self.url, {"refresh": str(self.refresh_token)})
        access_token = response.data.get("access")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token)
        self.assertIsInstance(access_token, str)

    def test_refresh_token_without_data(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get("refresh"))

    def test_refresh_token_with_invalid_token(self):
        response = self.client.post(self.url, {"refresh": "dummyRefreshToken"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
