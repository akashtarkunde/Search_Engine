from django.urls import path
from .views import search_page, search_products, upload_products

urlpatterns = [
    path('search/', search_page, name='search_page'),
    path('search-products/', search_products, name='search_products'),
    path('upload-products/', upload_products, name='upload_products')
]
