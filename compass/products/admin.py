from django.contrib import admin

from .models import Model_line, Product, Product_on_partner_status, Сategories


class Product_on_partnerInstanceInline(admin.TabularInline):
    model = Product_on_partner_status
    extra = 1
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'main_category',
        'model_line',
        'instruction')
    inlines = [Product_on_partnerInstanceInline, ]


@admin.register(Сategories)
class СategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Model_line)
class Model_lineAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product_on_partner_status)
class Product_on_partner_statusAdmin(admin.ModelAdmin):
    list_display=('product','partner', 'status')
