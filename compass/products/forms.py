from django.forms import ModelForm

from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        fields_required = ("name", "main_category", "model_line",)
