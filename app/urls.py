from django.urls import path

from app.apps import AppConfig
from app.views import all_products, contacts, product_card

app_name = AppConfig.name

urlpatterns = [
    path('', all_products, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pr_id>/', product_card, name='product_card'),
]