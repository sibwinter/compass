import os
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from ftplib import FTP
from pathlib import Path

import requests
from products.parser import get_products_dict

from partners.models import Partner
from .forms import ProductForm
from compass.settings import MEDIA_ROOT
from compass.settings import BASE_DIR, MEDIA_URL


from .models import Model_line, Product, Product_on_partner_status, Сategories


def pagination(products, page_number):
    """ Функция для формирования пагинации на странице."""
    paginator = Paginator(products, 10)
    return paginator.get_page(page_number)

def index(request):
    template = 'products/index.html'
    description = 'Продукция фабрики'
    products = Product.objects.all().select_related('model_line', 'main_category')
    context = {
        'page_obj': pagination(products, request.GET.get('page')),
        'description': description
    }
    return render(request, template, context)

def product_detail(request, product_pk):
    template = 'products/product_detail.html'
    description = 'Подробнее о товаре'
    
    product = get_object_or_404(
        Product,
        pk=product_pk
    )
    statuses = Product_on_partner_status.objects.filter(product=product) 
    if product.instruction:
        url = product.instruction.url
        current_path = os.path.dirname(product.instruction.url)
        url = os.path.join(current_path, url)
        site_url = 'https://compass-shop.ru/pdf/' + product.model_line.slug + '/' + os.path.basename(url)
        is_on_server = requests.get(site_url).status_code == 200
    else:
        url = 'Null'
        site_url = 'Null'
        is_on_server = False
    context = {
        'product': product,
        'description': description,
        'statuses': statuses,
        'url': url,
        'site_url': site_url,
        'is_on_server': is_on_server

    }
    return render(request, template, context)

def shoot_instruction_to_server(request, product_pk):
    product = get_object_or_404(
        Product,
        pk=product_pk
    )

    ftp = FTP('45.84.226.237')  # connect to host, default port
    ftp.login('admin_2', 'qg2op6X9fQ') 
    ftp.cwd('public_html/pdf') 
    

    url = product.instruction.path
    name = os.path.basename(url)
    slug = product.model_line.slug
    if  slug not in ftp.nlst():
        ftp.mkd(slug)
    ftp.cwd(slug)
    current_path = os.path.dirname(__file__)
    file_path = os.path.join(current_path, url)
    with open(file_path, 'rb') as file:
        ftp.storbinary(f'STOR {name}', file)    
    return redirect(reverse('products:product_detail', args=[product.pk]))

@csrf_protect
def product_create(request):
    form = ProductForm(request.POST or None,
                       files=request.FILES or None,)
    if form.is_valid():
        product = form.save(commit=False)
        product.save()
        return redirect(reverse('products:product_detail', args=[product.pk]))

    return render(request, 'products/product_create.html', {'form': form})


def product_edit(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    # if product.author == request.user:
    form = ProductForm(
        request.POST or None,
        files=request.FILES or None,
        instance=product
    )
    if form.is_valid():
        product.save()
        return redirect(reverse('products:product_detail', args=[product_pk]))
    return render(request,
                    'products/product_create.html',
                    {'form': form, 'is_edit': True})


def model_line_detail(request, model_line_pk):
    template = 'products/model_line_detail.html'
    description = 'Подробнее о линейке'
    
    model_line = get_object_or_404(
        Model_line,
        pk=model_line_pk
    )

    partners = [object for object in Partner.objects.all()]
    counts: dict = {}  # Словарь значений {Модельная линейка: кол-во товаров у партнера}

    for partner in partners:
        current_count = (Product_on_partner_status.objects
            .filter(partner=partner)
            .filter(product__model_line=model_line)
            .filter(status=True)
            .count()
        )
        total_count = model_line.products.count()
        counts[partner] = (current_count, total_count)
        

    context = {
        'partners': partners,
        'model_line': model_line,
        'counts': counts,        
    }
    return render(request, template, context)

def model_lines(request):
    template = 'products/model_lines.html'
    description = 'Модельные линейки мебельно фабрики Компасс'
    model_lines = [object for object in Model_line.objects.all()]
    counts: dict = {}
    for line in model_lines:
        """current_count = (Product_on_partner_status.objects
                .filter(product__model_line=line)
                .filter(status=True)
                .count()
            )"""
        total_count = (Product.objects
                .filter(model_line=line)
                .count()
            )
        counts[line] =  total_count
    context = { 
        'counts': counts,
        'description': description
    }
    return render(request, template, context)


def product_import(request):
    feed = get_products_dict()

    for sku, params in feed.items():
        category,created = Сategories.objects.get_or_create(name=params['category'])   
        print(category, created)
        model_line,created = Model_line.objects.get_or_create(name=params['model_line'])  
        model_line.save()   
       # print(model_line)
        category.save()   
        """product, created = Product.objects.get_or_create(
            main_category = category,
            model_line = model_line,
            name = params['name']
        )
        product.save()"""
       # print(product)
    return redirect(reverse('products:index'))