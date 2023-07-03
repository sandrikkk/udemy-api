# from django.contrib.auth.hashers import make_password
# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework_simplejwt.tokens import RefreshToken
#
# from apps.users.models import User
#
#
# class RegistrationTestCase(APITestCase):
#     def setUp(self):
#         self.url = "/user/registration/"
#
#     def test_registration(self):
#         data = {
#             "username": "example",
#             "email": "test12344@test.com",
#             "name": "test12345",
#             "password": "123",
#             "password_confirm": "123",
#         }
#         response = self.client.post(self.url, data)
#         response_data = response.data
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response_data.get("email"), data.get("email"))
#         self.assertListEqual(
#             list(response_data.keys()), ["id", "username", "email", "name", "isAdmin"]
#         )
#
#     def test_registration_with_existing_email(self):
#         User.objects.create(
#             username="existinguser",
#             email="existing@example.com",
#             password=make_password("existingpass"),
#         )
#         data = {
#             "username": "existinguser",
#             "email": "existing@example.com",
#             "password": "newpassword",
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(User.objects.count(), 1)
#         User.objects.get(email="existing@example.com").delete()
#
#
# class JWTAuthenticationTestCase(APITestCase):
#     def test_bearer_token(self):
#         user = User.objects.create(email="test@user.me", password="12345678")
#
#         refresh = RefreshToken.for_user(user)
#         return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
#
#
# class TestLogin(APITestCase):
#     def setUp(self):
#         self.url = "/user/login/"
#
#     def test_login_success(self):
#         User.objects.create(
#             email="test1234@gmail.com", password=make_password("test1234")
#         )
#         data = {"email": "test1234@gmail.com", "password": "test1234"}
#         response = self.client.post(self.url, data)
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("access", response.data)
#         User.objects.get(email="test1234@gmail.com").delete()
#
#     def test_login_invalid_credentials(self):
#         data = {"email": "invalid@gmail.com", "password": "invalid123"}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_login_missing_fields(self):
#         data = {}
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("email", response.data)
#         self.assertIn("password", response.data)
#         self.assertEqual(response.data["email"][0], "This field is required.")
#         self.assertEqual(response.data["password"][0], "This field is required.")
#
#     def test_inactive_users(self):
#         data = {
#             "email": "test1234@gmail.com",
#             "password": "test1234",
#             "is_active": False,
#         }
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(
#             response.data["detail"],
#             "No active account found with the given credentials",
#         )
