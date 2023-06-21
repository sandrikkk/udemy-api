from django.db import models
from django.contrib.auth.models import AbstractUser,User
from apps.base.models import BaseModelClass


class User(AbstractUser, BaseModelClass):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
