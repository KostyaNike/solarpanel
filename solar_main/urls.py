from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_page, name='form'),
    path('products/', views.products_page, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]