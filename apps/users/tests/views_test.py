# from unittest.mock import patch
#
# from django.urls import reverse
# from gaussportal.errors import InvalidTokenError, UserNotFoundError
# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework_simplejwt.tokens import RefreshToken
# from users.factories import UserFactory
# from users.models import User
#
#
# class LoginViewTestCase(APITestCase):
#     EMAIL_KEY = "email"
#     PASSWORD_KEY = "password"
#
#     def setUp(self) -> None:
#         self.url = reverse("token_obtain_pair")
#         self.user = UserFactory.create()
#         self.login_data = self._generate_login_data(self.user.email, "superPassword")
#
#     def test_user_login(self):
#         response = self.client.post(self.url, data=self.login_data)
#         response_data = response.data
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertListEqual(list(response_data.keys()), ["refresh", "access"])
#         self.assertIsInstance(response_data.get("refresh"), str)
#         self.assertIsInstance(response_data.get("access"), str)
#
#     def test_user_login_without_login_data(self):
#         response = self.client.post(self.url)
#         response_data = response.data
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertListEqual(
#             list(response_data.keys()), [self.EMAIL_KEY, self.PASSWORD_KEY]
#         )
#
#     def test_user_login_with_invalid_email(self):
#         response = self.client.post(
#             self.url, self._generate_login_data("someuseremail@example.com", "12345678")
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_user_login_with_incorrect_password(self):
#         response = self.client.post(
#             self.url, self._generate_login_data(self.user.email, "incorrectPass")
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def _generate_login_data(self, email: str, password: str) -> dict:
#         return {self.EMAIL_KEY: email, self.PASSWORD_KEY: password}
#
#
# class TokenRefreshViewTestCase(APITestCase):
#     def setUp(self) -> None:
#         self.url = reverse("token_refresh")
#         self.login_url = reverse("token_obtain_pair")
#         self.user = UserFactory.create()
#         self.refresh_token = RefreshToken.for_user(self.user)
#
#     def test_refresh_token_retrieval(self):
#         response = self.client.post(self.url, {"refresh": str(self.refresh_token)})
#         access_token = response.data.get("access")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIsNotNone(access_token)
#         self.assertIsInstance(access_token, str)
#
#     def test_refresh_token_without_data(self):
#         response = self.client.post(self.url)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIsNotNone(response.data.get("refresh"))
#
#     def test_refresh_token_with_invalid_token(self):
#         response = self.client.post(self.url, {"refresh": "dummyRefreshToken"})
#
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class RegisterViewTestCase(APITestCase):
#     def setUp(self) -> None:
#         self.url = reverse("register")
#         self.request_data = {
#             "username": "testUserName",
#             "email": "testUserEmail@example.com",
#             "role": "administrator",
#             "password": "superPassword",
#             "password_confirm": "superPassword",
#         }
#         self.response_keys = ["id", "username", "email", "role"]
#
#     def test_user_registration(self):
#         response = self.client.post(self.url, self.request_data)
#         response_data = response.data
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertListEqual(list(response_data.keys()), self.response_keys)
#         self.assertEqual(response_data.get("email"), self.request_data.get("email"))
#         self.assertEqual(response_data.get("role"), self.request_data.get("role"))
#         self.assertEqual(
#             response_data.get("username"), self.request_data.get("username")
#         )
#         self.assertEqual(response_data.get("id"), User.objects.last().id)
#
#     def test_user_registration_without_data(self):
#         response = self.client.post(self.url)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertListEqual(list(response.data.keys()), list(self.request_data.keys()))
#
#     def test_user_with_existing_username(self):
#         self._test_user_with_existing_attributes("username")
#
#     def test_user_with_existing_email(self):
#         self._test_user_with_existing_attributes("email")
#
#     def _test_user_with_existing_attributes(self, attribute_name: str):
#         user = UserFactory.create()
#         self.request_data[attribute_name] = getattr(user, attribute_name)
#         response = self.client.post(self.url, self.request_data)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIsNotNone(response.data.get(attribute_name))
