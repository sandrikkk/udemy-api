from django.db import models

from apps.base.models import BaseModelClass
from apps.category.models import Category


class Product(BaseModelClass):
    name = models.CharField(max_length=256, unique=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products", null=True
    )
    description = models.TextField(
        max_length=512,
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.ImageField(upload_to="uploads/", blank=True, null=True)

    def __str__(self):
        return self.name
