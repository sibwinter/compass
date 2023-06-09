from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('products/product_create/', views.product_create, name='product_create'),
    path('products/<int:product_pk>/to_server', views.shoot_instruction_to_server, name='shoot_instruction_to_server'),
]
