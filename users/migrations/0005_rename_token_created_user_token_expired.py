# Generated by Django 4.1.5 on 2023-02-07 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_token_user_token_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='token_created',
            new_name='token_expired',
        ),
    ]