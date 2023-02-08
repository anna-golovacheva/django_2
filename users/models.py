from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=25, verbose_name='номер телефона')
    country = models.CharField(max_length=50, verbose_name='страна')
    token = models.CharField(max_length=15, **NULLABLE, verbose_name='токен')
    token_expired = models.DateTimeField(**NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
