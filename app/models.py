from django.db import models
from autoslug import AutoSlugField
from pytils.translit import slugify

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.CharField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена за покупку')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    changed_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Record(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Slug')
    content = models.CharField(max_length=500, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='records/', **NULLABLE, verbose_name='Превью')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)



