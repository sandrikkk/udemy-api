from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
