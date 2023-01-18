from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.CharField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    category =
    price =
    created_date =
    changed_date =




