from django.db import models

from apps.base.models import BaseModelClass
from apps.products.models import Product
from apps.users.models import User

STAR = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Review(BaseModelClass):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField(choices=STAR)
    comment = models.TextField()

    def __str__(self):
        return self.user.username
