import os
import uuid
from django.db import models
from slugify import slugify

# Create your models here.

def get_upload_path(instance, filename):
    new_name = slugify(filename[:-4])+'.pdf'

    return os.path.join('instructions/',instance.model_line.slug, new_name)


class Model_line(models.Model):
    """Модельная линейка."""
    AN = 'Анастасия'
    AS = 'Ассоль'
    DS = 'Дримстар'
    MODEL_LINES_NAMES = [
        (AN, 'Анастасия'),
        (AS, 'Ассоль'),
        (DS, 'Дримстар'),
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
        on_delete=models.CASCADE,
        related_name='product'
    )

    model_line = models.ForeignKey(
        Model_line,
        on_delete=models.CASCADE,
        related_name='product'
    )

    instruction = models.FileField(
        blank=True,
        verbose_name="Инструкция",
        upload_to=get_upload_path  # сохраняем файл в папку линейки
    )

    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'