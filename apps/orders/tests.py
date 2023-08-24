from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.category.models import Category
from apps.orders.models import Order
from apps.products.models import Product
from apps.users.models import User


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse("orders", kwargs={"pk": 1})
        self.user = User.objects.create(email="test1234@gmail.com", password=make_password("test1234"))
        self.user.is_verified = True
        self.user.save()
        self.client.login(email="test1234@gmail.com", password="test1234")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Product 1",
            description="Description 1",
            price=9.99,
            category=self.category,
        )

    @patch("apps.orders.views.send_order_completion_email")
    def test_create_order(self, mock_send_order_completion_email):
        data = {"product": self.product.id, "user": self.user}

        # Send a POST request to create the order
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        mock_send_order_completion_email.delay.assert_called_once_with(self.user.email)
