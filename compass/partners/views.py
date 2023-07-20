import os
from django.shortcuts import get_object_or_404, render

from partners.models import Partner
from products.models import Model_line, Product_on_partner_status

# Create your views here.
def partner_detail(request, partner_pk):
    template = 'partners/partner_detail.html'
    description = 'Подробнее о партнере'
    
    partner = get_object_or_404(Partner,pk=partner_pk)
    model_lines = [object.name for object in Model_line.objects.all()]
    counts: dict = {}  # Словарь значений {Модельная линейка: кол-во товаров у партнера}
    for line in model_lines:
        current_count = (Product_on_partner_status.objects
            .filter(partner=partner)
            .filter(product__model_line__name=line)
            .filter(status=True)
            .count()
        )
        total_count = (Model_line.objects
            .get(name=line)
            .products
            .count()
        )
        counts[line] = (current_count, total_count)
    context = {
        'partner': partner,
        'counts': counts,     

    }
    return render(request, template, context)

def index(request):
    template = 'partners/index.html'
    description = 'Партнеры мебельной фабрики Компасс'
    partners = [object for object in Partner.objects.all()]
    counts: dict = {}
    main_table = {}
    for partner in partners:
        total_count = (Product_on_partner_status.objects
                .filter(status=True)
                .filter(partner=partner)
                .count()
            )
        counts[partner] =  total_count
        lines = [object for object in Model_line.objects.all()]
        lines_count={}
        for line in lines:
            lines_count[line] = (Product_on_partner_status.objects
                                          .filter(product__model_line=line)
                                          .filter(partner=partner)
                                          .filter(status=True)
                                          .count())
        main_table[partner] = lines_count

    context = { 
        'counts': counts,
        'lines': lines,
        'main_table': main_table,
        'description': description
    }
    return render(request, template, context)