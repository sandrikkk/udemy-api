from django.db import models
from django.test import TestCase

from apps.category.models import Category
from apps.products.models import Product


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Programming")

        Product.objects.create(
            name="Not Bad Course", category=category, description="Good", price="15"
        )

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field("name").max_length
        self.assertEqual(max_length, 256)

    def test_name_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "category")

    def test_category_related_name(self):
        product = Product.objects.get(id=1)
        category_field = product._meta.get_field("category")
        related_name = category_field.remote_field.related_name
        self.assertEqual(related_name, "products")

    def test_category_on_delete(self):
        product = Product.objects.get(id=1)
        category_field = product._meta.get_field("category")
        on_delete = category_field.remote_field.on_delete
        self.assertEqual(on_delete, models.DO_NOTHING)
