from django.contrib import admin

from .models import Model_line, Product, Сategories


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'main_category',
        'model_line',
        'instruction')
    
@admin.register(Сategories)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name',)


@admin.register(Model_line)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name',)
