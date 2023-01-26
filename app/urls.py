from django.urls import path

from app.apps import AppConfig
from app.views import contacts, ProductListView, ProductDetailView, \
    RecordCreateView, RecordUpdateView, RecordListView, RecordDetailView, \
    RecordDeleteView

app_name = AppConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_card'),
    path('records/', RecordListView.as_view(), name='records'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_card'),
    path('records_create/', RecordCreateView.as_view(), name='create_record'),
    path('records_update/<slug:slug>/', RecordUpdateView.as_view(), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
]