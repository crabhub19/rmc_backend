from django.urls import path, include
from .views import *
urlpatterns = [
    path('products',ProductList.as_view(),name='products'),
    path('product_details/<str:slug>',ProductDetail,name='product_details'),
]