from unittest.mock import patch

from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from apps.category.models import Category
from apps.orders.models import Order
from apps.products.models import Product
from apps.users.models import User
from django.urls import reverse


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("orders", kwargs={"pk": 1})
        self.user = User.objects.create(
            email="test1234@gmail.com", password=make_password("test1234")
        )
        self.client.login(email="test1234@gmail.com", password="test1234")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Product 1",
            description="Description 1",
            price=9.99,
            category=self.category,
        )

    @patch("apps.orders.serializers.send_order_completion_email")
    def test_create_order(self, mock_send_order_completion_email):
        # Define the data for the order
        data = {
            "product": self.product.id,
            "user": self.user,
        }

        # Send a POST request to create the order
        response = self.client.post(self.url, data)

        # Assert that the order was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        # Assert that the send_order_completion_email function was called
        mock_send_order_completion_email.delay.assert_called_once_with(self.user.email)
