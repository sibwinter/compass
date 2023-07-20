import os
from django.forms import modelformset_factory
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.db.models.functions import Lower
from django.utils import timezone
from ftplib import FTP
from pathlib import Path
from .partner_parser import find_price_stolplit

import plotly.express as px
import plotly.graph_objects as go

from dotenv import load_dotenv
load_dotenv()

import requests
from products.parser import get_products_dict

from partners.models import Partner
from .forms import ProductForm, ProductOnPartnerStatusForm
from compass.settings import MEDIA_ROOT
from compass.settings import BASE_DIR, MEDIA_URL


from .models import Model_line, Product, Product_on_partner_status, Progress, Сategories


def pagination(products, page_number):
    """ Функция для формирования пагинации на странице."""
    paginator = Paginator(products, 25)
    return paginator.get_page(page_number)

def get_chart():
    progress = Progress.objects.all().order_by('date')
    fig1 = px.line(
        x=[today_prog.date for today_prog in progress],
        y=[today_prog.have_not_packeges_demensions_count for today_prog in progress],
        color_discrete_sequence = ['blue'],
        labels={'x': 'Дата', 'y': 'нет размеров упаковок'}
    )
    fig2 = px.line(
        x=[today_prog.date for today_prog in progress],
        y=[today_prog.have_not_packeges_count for today_prog in progress],
        color_discrete_sequence = ['red'],
        labels={'x': 'Дата', 'y': 'нет кол-во упаковок'}
    )
    fig3 = px.line(
        x=[today_prog.date for today_prog in progress],
        y=[today_prog.have_not_weight_count for today_prog in progress],
        color_discrete_sequence = ['green'],
        labels={'x': 'Дата', 'y': 'нет веса'}
    )

    fig = go.Figure(data=fig1.data + fig2.data + fig3.data)

    chart = fig.to_html()
    return chart

def index(request):
    template = 'products/index.html'
    description = 'Продукция фабрики'
    query = request.GET.get('q')
    is_have_packeges = Product.objects.filter(packaging_demensions='').count()
    is_have_packeges_count = Product.objects.filter(packaging_count=None).count()
    is_have_weight_count = Product.objects.filter(weight=None).count()
    is_have_width_count = Product.objects.filter(width=None).count()
    is_have_height_count = Product.objects.filter(height=None).count()
    is_have_depth_count = Product.objects.filter(depth=None).count()
    is_have_instruction_count = Product.objects.filter(instruction=None).count()
    products = Product.objects.all().select_related('model_line', 'main_category')
    if query is not None:
        products = (Product.objects.annotate(name_lower=Lower('name')) #not working with SQlite
                                   .select_related('model_line', 'main_category')
                                   .filter(name_lower__icontains=query)
                                   .order_by('id')
        )
    context = {
        'page_obj': pagination(products, request.GET.get('page')),
        'description': description,
        'is_have_packeges': is_have_packeges,
        'is_have_packeges_count': is_have_packeges_count,
        'is_have_weight_count': is_have_weight_count,
        'is_have_width_count': is_have_width_count,
        'is_have_height_count': is_have_height_count,
        'is_have_depth_count': is_have_depth_count,
        'is_have_instruction_count': is_have_instruction_count,
        'query':query,
        'chart': get_chart()
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
    #ищем товар на столплите:
    

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

    attributes = product.__iter__
    """attributes['Цена']=product.price.__iter__
    attributes['main_category']=product.main_category
    attributes['sku']=product.sku
    attributes['name']=product.name
    attributes['url']=product.url
    attributes['description']=product.description
    attributes['barcode']=product.barcode
    attributes['dimensions']=product.dimensions
    attributes['model_line']=product.model_line
    attributes['height']=product.height
    attributes['width']=product.width
    attributes['depth']=product.depth
    attributes['weight']=product.weight"""
    context = {
        'product': product,
        'attributes': attributes,
        'statuses': statuses,
        'site_url': site_url,
        'is_on_server': is_on_server,

    }
    return render(request, template, context)

def shoot_instruction_to_server(request, product_pk):
    product = get_object_or_404(
        Product,
        pk=product_pk
    )

    print(os.getenv('FTP_HOST'),os.getenv('FTP_LOGIN'), os.getenv('FTP_PASSWORD'),os.getenv('FTP_PATH')) 
  
    ftp = FTP(os.getenv('FTP_HOST'))  # connect to host, default port
    ftp.login(os.getenv('FTP_LOGIN'), os.getenv('FTP_PASSWORD')) 
    ftp.cwd(os.getenv('FTP_PATH')) 
    

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
    """Редактируем товар в наешй базе."""
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


def product_in_partners_edit(request, product_pk):
    """Редактируем наличие товара у поставщиков."""
    product = get_object_or_404(Product, pk=product_pk)
    """product_in_partners = get_object_or_404(Product_on_partner_status, product=product)
    form = ProductOnPartnerStatusForm(request.POST or None,)"""
    context ={}

    variants_stolplit: dict = find_price_stolplit(product.sku[0:5])

    # Если найдет только один вариант то сразу обновляем статус и добавляем ссылку и цену
    if len(variants_stolplit) == 1:
        product_to_edit = Product_on_partner_status.objects.get(
                            product=product,
                            partner__name='Столплит')
        print(product_to_edit)
        product_to_edit.price = next(iter(variants_stolplit.values()))[0]
        product_to_edit.link = next(iter(variants_stolplit.values()))[1]
        product_to_edit.status = True
        product_to_edit.save()

    print(variants_stolplit)

    # creating a formset and 5 instances of GeeksForm
    ProductInPartnersFormSet = modelformset_factory(
        Product_on_partner_status, 
        fields =('partner', 'status', 'link', 'price'),
        widgets = {'status':forms.CheckboxInput, },
        
        extra=0,
    )
    
    formset = ProductInPartnersFormSet(
        request.POST or None,
        queryset=Product_on_partner_status.objects.filter(product=product),
        #initial=[{'link': next(iter(variants_stolplit.values()))[1],
        #         'price': float(next(iter(variants_stolplit.values()))[0].replace(' ', ''))}],
    )
    print(formset.is_valid() )
    context['formset'] = formset
    context['product'] = product
    context['variants_stolplit'] = variants_stolplit
    if formset.is_valid():
        instances = formset.save()
        return redirect(reverse('products:product_detail', args=[product_pk]))
        
    return render(request,
                      'products/products_in_partners_edit.html',
                      context)


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
        
    products = model_line.products.all()
       
    context = { 
        'page_obj': pagination(products, request.GET.get('page')),
        'description': description,
        'partners': partners,
        'products':products,
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
    """Функция импорта товаров сз фида сайта в формате xml.
    
    Метод позволяет создать новые товары в базе данных или обновить существующие.
    todo: добавить уведомление о кол-ве обновленных и добавленных товаров
    """
    feed = get_products_dict()

    for sku, params in feed.items():
        cat_name = params['category'] if params['category'] is not None and len(params['category']) > 0 else 'Default'
        category, created = Сategories.objects.get_or_create(name=cat_name)
        
        model_line_name = params['model_line'] if params['model_line'] is not None and len(params['model_line']) > 0 else 'Default'
        model_line, created = Model_line.objects.get_or_create(name=model_line_name)
        
        #print(model_line, category, created)
        product, created = Product.objects.get_or_create(id=params['id'])
        
        if product:
            product.price = params['price']
            product.main_category = category
            product.sku = sku
            product.name = params['name']
            product.url = params['url']
            product.description = params['description']
            product.barcode = ''.join(params['barcode'])
            product.dimensions = ''.join(params['dimensions'])
            product.packaging_demensions = ''.join(params['packaging_demensions'])
            product.packaging_count = int(params['packaging_count'].replace(',', '.')) if len(params['packaging_count']) > 0 else None
            product.model_line = model_line
            product.height = float(params['height'].replace(',', '.')) if len(params['height']) > 0 else None
            product.width = float(params['width'].replace(',', '.').replace('-', '.')) if len(params['width']) > 0 else None
            product.depth = float(params['depth'].replace(',', '.')) if len(params['depth']) > 0 else None
            product.weight = float(params['weight'].replace(',', '.')) if len(params['weight']) > 0 else None

        product.save()
        print(product.name, product.packaging_count, created)
       # print(product)
    return redirect(reverse('products:index'))


def products_with_problem(request, problem_parameter):
    template = 'products/problem_parameter.html'
    if problem_parameter == 'packaging_demensions':
        products = Product.objects.filter(packaging_demensions='').order_by('model_line')
    if problem_parameter == 'packaging_count':
        products = Product.objects.filter(packaging_count=None).order_by('model_line')
    if problem_parameter == 'weight':
        products = Product.objects.filter(weight=None).order_by('model_line')
    if problem_parameter == 'height':
        products = Product.objects.filter(height=None).order_by('model_line')
    if problem_parameter == 'width':
        products = Product.objects.filter(width=None).order_by('model_line')
    if problem_parameter == 'depth':
        products = Product.objects.filter(depth=None).order_by('model_line')
    if problem_parameter == 'instruction':
        products = Product.objects.filter(instruction=None).order_by('model_line')
        
    description = (f'Проблемы с параметром {problem_parameter}. '
                   f'Найдено {products.count()} ошибок'
                   )
    context = {
        'page_obj': pagination(products, request.GET.get('page')),
        'description': description,
    }
    return render(request, template, context)




def create_new_progress(request):
    # нужно допилить автоматическое создание по расписанию или по кнопке
    progress, created = Progress.objects.get_or_create(
        date=timezone.now().date()
    )

    progress.have_not_depth_count = Product.objects.filter(depth=None).count()
    progress.have_not_height_count = Product.objects.filter(height=None).count()
    progress.have_not_packeges_count = Product.objects.filter(packaging_count=None).count()
    progress.have_not_packeges_demensions_count = Product.objects.filter(packaging_demensions='').count()    
    progress.have_not_weight_count = Product.objects.filter(weight=None).count()
    progress.have_not_width_count = Product.objects.filter(width=None).count()
    progress.save()
    return redirect(reverse('products:index'))


def stolplit_find_products(request):
    products = Product.objects.all()
    count = 0
    for product in products:

        variants_stolplit: dict = find_price_stolplit(product.sku[0:5])
        # Если найдет только один вариант то сразу обновляем статус и добавляем ссылку и цену
        if len(variants_stolplit) == 1:
            product_to_edit = Product_on_partner_status.objects.get(
                                product=product,
                                partner__name='СТОЛПЛИТ')
            print(product_to_edit)
            product_to_edit.price = next(iter(variants_stolplit.values()))[0]
            product_to_edit.link = next(iter(variants_stolplit.values()))[1]
            product_to_edit.status = True
            product_to_edit.save()
            count += 1
    print(f'добавлено {count} соотвествий')
    return redirect(reverse('products:index'))