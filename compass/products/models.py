import os
import uuid
from django.db import models
from django.db.models import UniqueConstraint
from slugify import slugify
from django.utils import timezone

from partners.models import Partner





def get_upload_path(instance, filename):
    new_name = slugify(filename[:-4])+'.pdf'

    return os.path.join('instructions/', instance.model_line.slug, new_name)


class Model_line(models.Model):
    """Модельная линейка."""
    
    AS = 'Ассоль'
    AT = 'Агата'
    AN = 'Анастасия'
    VI = 'Виктория'
    DS = 'Дримстар'
    IZ = 'Изабель'
    IR = 'Ирма'
    MB = 'Монблан'
    OF = 'Офис'
    SL = 'Скайлайт'
    SO = 'Соня Премиум'
    EM = 'Элизабет'
    EL = 'Эмилия'
    MODEL_LINES_NAMES = [
        (AS, 'Ассоль'),
        (AT, 'Агата'),
        (AN, 'Анастасия'),
        (VI, 'Виктория'),
        (DS, 'Дримстар'),
        (IZ, 'Изабель'),
        (IR, 'Ирма'),
        (MB, 'Монблан'),
        (OF, 'Офис'),
        (SL, 'Скайлайт'),
        (SO, 'Соня Премиум'),
        (EM, 'Элизабет'),
        (EL, 'Эмилия'),
    ]
    name = models.CharField(
        #  choices=MODEL_LINES_NAMES, -
        verbose_name='Наименование категории',
        max_length=250,
        unique=True,
        blank=True,
        null=True,
        default='Default'
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
        blank=True,
        null=True,
        default=uuid.uuid1
    )

    class Meta:
        verbose_name = 'Модельная линейка'
        verbose_name_plural = 'Модельные линейки'

    def __str__(self):
        return f'{self.name}'


class Сategories(models.Model):
    """Категория продукции."""
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=250,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


class Product(models.Model):
    """Продукция фабрики."""
    name = models.CharField(
        verbose_name='Наименование продукции',
        max_length=250,
        unique=True,
    )
    main_category = models.ForeignKey(
        Сategories,
        blank=True,
        null=True,
        verbose_name='Главная категория',
        on_delete=models.CASCADE,
        related_name='products'
    )
    model_line = models.ForeignKey(
        Model_line,
        blank=True,
        null=True,
        verbose_name='Модельная линейка',
        on_delete=models.CASCADE,
        related_name='products'
    )
    instruction = models.FileField(
        blank=True,
        null=True,
        verbose_name="Инструкция",
        upload_to=get_upload_path  # сохраняем файл в папку линейки
    )
    price = models.FloatField(
        verbose_name='Цена, руб.',
        blank=True,
        null=True,
    )
    sku = models.CharField(
        verbose_name='Артикул сайта',
        max_length=250,
        unique=True,
        blank=True,
        null=True
    )
    url = models.CharField(
        verbose_name='Ссылка на сайт',
        max_length=250,
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Описание товара',
        blank=True,
    )
    dimensions = models.CharField(
        verbose_name='Габариты',
        max_length=250,
        blank=True,
    )
    height = models.FloatField(
        verbose_name='Высота изделия, см.',
        blank=True,
        null=True
    )
    width = models.FloatField(
        verbose_name='Ширина изделия, см.',
        blank=True,
        null=True
    )
    depth = models.FloatField(
        verbose_name='Глубина изделия, см.',
        blank=True,
        null=True
    )
    barcode = models.CharField(
        verbose_name='Штрихкоды',
        max_length=500,
        blank=True,
        null=True
    )
    weight = models.FloatField(
        verbose_name='Вес изделия, кг.',
        blank=True,
        null=True
    )
    packaging_demensions = models.CharField(
        verbose_name='Габариты упаковок',
        max_length=500,
        blank=True,
        null=True
    )
    packaging_count = models.SmallIntegerField(
        verbose_name='Количество упаковок',
        blank=True,
        null=True
    )
    site_id = models.IntegerField(
        verbose_name='ID товара с сайта',
        blank=True,
        unique=True,
        null=True
    )
    def __str__(self):
        return self.name
    
    def __iter__(self):
        for field in self._meta.fields:
            yield (field.verbose_name, field.value_to_string(self))
            
    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'
        


class Product_on_partner_status(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name='partner_status',        
        null=True
    )
    status = models.BooleanField(
        verbose_name="Залит на сайт",
        blank=True,
        default=False,
        null=True
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name="Партнер",
        on_delete=models.CASCADE,
        related_name='partner_status',
        blank=True,
        null=True
    )
    link = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='ссылка на продукт у партнера'
    )

    def __str__(self):
        return f'{self.partner.name} - Залито' if self.status else f'{self.partner.name} - Не залито'

    class Meta:
        verbose_name = 'Продукция у партнера'
        verbose_name_plural = 'Продукция у партнера'
        """constraints = [
            UniqueConstraint(
                fields=['product', 'partner'],
                name='unique_product_status'),
        ]"""


class Progress(models.Model):
    date = models.DateField(
        verbose_name='дата',
        auto_created=True,
        default=timezone.now().date()
        )
    have_not_packeges_demensions_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено кол-во упаковок'
        )
    have_not_packeges_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено размеров упаковок'
        )
    have_not_weight_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено вес'
        )
    have_not_width_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено ширина'
        )
    have_not_height_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено высота'
        )
    have_not_depth_count = models.PositiveSmallIntegerField(
        verbose_name='не заполнено глубина'
        )
