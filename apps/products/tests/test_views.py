from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase

from apps.category.models import Category
from apps.products.models import Product
from apps.users.models import User


class ProductCreationAPITestCase(APITestCase):
    def setUp(self):
        self.url = "/products/"
        self.user = User.objects.create(
            email="test1234@gmail.com", password=make_password("test1234")
        )
        self.client.login(email="test1234@gmail.com", password="test1234")

    def test_product_creation(self):
        # Create a category for the product
        category = Category.objects.create(name="history")

        # Define the data for the product
        data = {
            "name": "good course",
            "description": "the best description ever",
            "price": "25.00",
            "category": category.id,
        }

        # Send a POST request to create the product
        response = self.client.post(self.url, data)

        # Assert that the product was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        # Assert that the response data contains the expected keys
        response_data = response.data
        expected_keys = [
            "id",
            "created_at",
            "updated_at",
            "deleted",
            "name",
            "description",
            "price",
            "images",
            "category",
        ]
        self.assertListEqual(list(response_data.keys()), expected_keys)


class ProductRetrievalAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test1234@gmail.com", password=make_password("test1234")
        )
        self.client.login(email="test1234@gmail.com", password="test1234")
        self.category = Category.objects.create(name="Electronics")

        self.product1 = Product.objects.create(
            name="Product 1",
            description="Description 1",
            price=9.99,
            category=self.category,
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            description="Description 2",
            price=19.99,
            category=self.category,
        )
        self.product3 = Product.objects.create(
            name="Product 3",
            description="Description 3",
            price=29.99,
            category=self.category,
        )

    def test_retrieve_product_by_id(self):
        # Retrieve the product by its ID
        retrieved_product = Product.objects.get(id=self.product1.id)

        # Assert that the retrieved product has the expected attributes
        self.assertEqual(retrieved_product.name, "Product 1")
        self.assertEqual(retrieved_product.description, "Description 1")
        self.assertEqual(retrieved_product.category, self.category)

    def test_retrieve_product_by_name(self):
        # Retrieve the product by its name
        retrieved_product = Product.objects.get(name="Product 2")

        # Assert that the retrieved product has the expected attributes
        self.assertEqual(retrieved_product.name, "Product 2")
        self.assertEqual(retrieved_product.description, "Description 2")
        self.assertEqual(retrieved_product.category, self.category)
