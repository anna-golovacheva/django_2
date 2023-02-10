# Generated by Django 4.1.5 on 2023-02-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_product_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.CharField(choices=[('published', 'опубликован'), ('not published', 'не опубликован')], default='not published', max_length=20),
        ),
    ]
