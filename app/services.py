import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.mail import send_mail

from app.models import Category


def get_categories_from_cache():
    queryset = Category.objects.all()

    if settings.CACHE_ENABLED:
        key = 'categories'
        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)

        return cache_data

    return queryset


def set_registration(form, obj):
    password = form.data.get('password')
    obj.set_password(password)
    obj.token = make_password(obj.password)[-15:]
    obj.token_expired = datetime.datetime.now().astimezone() + datetime.timedelta(hours=72)
    obj.is_active = False
    return obj


def send_register_mail(message, email):
    send_mail(
        subject='активация',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
