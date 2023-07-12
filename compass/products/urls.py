from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_pk>/', views.product_detail, name='product_detail'),
    path('products/problem_parameter/<str:problem_parameter>/', views.products_with_problem, name='products_with_problem'),
    path('products/import/', views.product_import, name='product_import'),
    path('products/<int:product_pk>/edit', views.product_edit, name='product_edit'),
    path('products/<int:product_pk>/partners', views.product_in_partners_edit, name='product_in_partners_edit'),
    path('products/product_create/', views.product_create, name='product_create'),
    path('products/<int:product_pk>/to_server', views.shoot_instruction_to_server, name='shoot_instruction_to_server'),
    path('products/model_lines/<int:model_line_pk>', views.model_line_detail, name='model_line_detail'),
    path('products/model_lines/', views.model_lines, name='model_lines'),
    path('products/new_progress/', views.create_new_progress, name='create_new_progress'),
]
