from django.urls import path
from .views import search_page, search_products

urlpatterns = [
    path('search/', search_page, name='search_page'),
    path('search-products/', search_products, name='search_products'),
]
