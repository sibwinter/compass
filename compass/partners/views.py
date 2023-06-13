import os
from django.shortcuts import get_object_or_404, render

from compass.partners.models import Partner
from compass.products.models import Product_on_partner_status

# Create your views here.
def product_detail(request, product_pk):
    template = 'partners/partner_detail.html'
    description = 'Подробнее о партнере'
    
    product = get_object_or_404(
        Partner,
        pk=product_pk
    )
    statuses = Product_on_partner_status.objects.filter(product=product) 
    url = product.instruction.url
    current_path = os.path.dirname(product.instruction.url)
    url = os.path.join(current_path, url)
    site_url = 'https://compass-shop.ru/pdf/' + product.model_line.slug + '/' + os.path.basename(url)
    is_on_server = requests.get(site_url).status_code == 200

    context = {
        'product': product,
        'description': description,
        'statuses': statuses,
        'url': url,
        'site_url': site_url,
        'is_on_server': is_on_server

    }
    return render(request, template, context)