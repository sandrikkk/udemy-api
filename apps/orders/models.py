from django.db import models

from apps.base.models import BaseModelClass
from apps.products.models import Product
from apps.users.models import User

STATUS = (
    ('SUCCEED', 'Succeed'),
    ('CANCELLED', 'Cancelled'),
)


class Order(BaseModelClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=20)

    def __str__(self):
        return f"{self.user}, {self.product}"
