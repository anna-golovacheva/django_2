from django.conf import settings
from django.db import models
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
    PUBLISHED = 'published'
    NOT_PUBLISHED = 'not published'
    PUBLISH_CHOICES = [(PUBLISHED, 'опубликован'), (NOT_PUBLISHED, 'не опубликован')]

    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.CharField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена за покупку')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    is_published = models.CharField(max_length=20, choices=PUBLISH_CHOICES, default=NOT_PUBLISHED)
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    changed_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('pk',)
        permissions = [
            (
                'set_published',
                'Can publish product'
            ),
            (
                'change_description',
                'Can change product description'
            ),
            (
                'change_category',
                'Can change product category'
            )
        ]

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


class Version(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название версии')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1, verbose_name='Продукт')
    is_active = models.BooleanField(verbose_name='Текущая версия')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    def __str__(self):
        return self.name


