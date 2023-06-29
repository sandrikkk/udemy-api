from django.test import TestCase
from rest_framework import status

from apps.category.models import Category
from apps.products.models import Product


class ProductCreationTestCase(TestCase):
    def setUp(self):
        self.url = "/products/"

    def test_product_creation(self):
        category = Category.objects.create(name="history")
        data = {
            "name": "good coursessssdasdssss",
            "description": "dsfasdfss",
            "price": "25.00",
            "category": category.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Product.objects.count(), 1)
        response_data = response.data
        print(response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(
            list(response_data.keys()),
            [
                "id",
                "created_at",
                "updated_at",
                "deleted",
                "name",
                "description",
                "price",
                "images",
                "category",
            ],
        )


class ProductRetrievalTestCase(TestCase):
    def setUp(self):
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
        retrieved_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(retrieved_product.name, "Product 1")
        self.assertEqual(retrieved_product.description, "Description 1")
        self.assertEqual(retrieved_product.category, self.category)

    def test_retrieve_product_by_name(self):
        retrieved_product = Product.objects.get(name="Product 2")
        self.assertEqual(retrieved_product.name, "Product 2")
        self.assertEqual(retrieved_product.description, "Description 2")
        self.assertEqual(retrieved_product.category, self.category)
