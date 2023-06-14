import os
import uuid
from django.db import models
from django.db.models import UniqueConstraint
from slugify import slugify

from partners.models import Partner


# Create your models here.


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
        choices=MODEL_LINES_NAMES,
        verbose_name='Наименование категории',
        max_length=250,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
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
        verbose_name='Главная категория',
        on_delete=models.CASCADE,
        related_name='products'
    )

    model_line = models.ForeignKey(
        Model_line,
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

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'


class Product_on_partner_status(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name='partner_status'
    )
    status = models.BooleanField(
        verbose_name="Залит на сайт"
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name="Партнер",
        on_delete=models.CASCADE,
        related_name='partner_status'
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
        constraints = [
            UniqueConstraint(
                fields=['product', 'partner'],
                name='unique_product_status'),
        ]
        
