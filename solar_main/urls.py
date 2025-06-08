from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_page, name='form'),
    path('products/', views.products_page, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)