from django import forms

from .models import Product, Product_on_partner_status


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        fields_required = ("name", "main_category", "model_line",)


class ProductOnPartnerStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductOnPartnerStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.CheckboxInput

    status = forms.BooleanField(widget=forms.CheckboxInput)
    class Meta:
        model = Product_on_partner_status
        fields = ('partner', 'status', 'link')
        widgets = {
            'status': forms.RadioSelect,
        }

    