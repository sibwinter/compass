from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('products/<int:product_pk>/edit', views.product_edit, name='product_edit'),
    path('products/product_create/', views.product_create, name='product_create'),
    path('products/<int:product_pk>/to_server', views.shoot_instruction_to_server, name='shoot_instruction_to_server'),
    path('products/model_lines/<int:model_line_pk>', views.model_line_detail, name='model_line_detail'),
    path('products/model_lines/', views.model_lines, name='model_lines'),
]
