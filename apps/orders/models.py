from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField

from apps.base.models import BaseModelClass
from apps.products.models import Product
from apps.users.models import User


class Status(ChoiceEnum):
    SUCCEED = "Succeed"
    CANCELLED = "Cancelled"


class Order(BaseModelClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = EnumChoiceField(Status, max_length=20)

    def __str__(self):
        return f"{self.user}, {self.product}"
