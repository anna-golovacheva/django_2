from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import cache_page

from app.apps import AppConfig
from app.views import contacts, ProductListView, ProductDetailView, \
    RecordCreateView, RecordUpdateView, RecordListView, RecordDetailView, \
    RecordDeleteView, ProductCreateView, ProductUpdateWithVersionView, \
    ProductDeleteView, change_is_published, ProductDescriptionUpdateView, \
    ProductCategoryUpdateView, CategoryListView

app_name = AppConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', login_required(contacts), name='contacts'),
    path('product_create/', login_required(ProductCreateView.as_view()), name='create_product'),
    path('product_update/<int:pk>/', login_required(ProductUpdateWithVersionView.as_view()), name='update_product'),
    path('product_update_description/<int:pk>/', login_required(ProductDescriptionUpdateView.as_view()), name='update_product_description'),
    path('product_update_category/<int:pk>/', login_required(ProductCategoryUpdateView.as_view()), name='update_product_category'),
    path('list_category/', login_required(CategoryListView.as_view()), name='list_category'),
    path('<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_card'),
    path('is_published/<int:pk>/', change_is_published, name='change_is_published'),
    path('product_delete/<int:pk>/', login_required(ProductDeleteView.as_view()), name='delete_product'),
    path('records/', RecordListView.as_view(), name='records'),
    path('records/<slug:slug>/', RecordDetailView.as_view(), name='record_card'),
    path('records_create/', RecordCreateView.as_view(), name='create_record'),
    path('records_update/<slug:slug>/', RecordUpdateView.as_view(), name='update_record'),
    path('records_delete/<slug:slug>/', RecordDeleteView.as_view(), name='delete_record'),
]