from django.urls import path

from app.apps import AppConfig
from app.views import all_products

app_name = AppConfig.name

urlpatterns = [
    path('', all_products),
    # path('contacts/', contacts)
]