from django.db import models


class Partner(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название партнера'
    )
    full_name_official = models.CharField(
        max_length=250,
        unique=True,
        blank=True,
        verbose_name='Полное название организации'
    )
    site = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Ссылка на сайт партнера'
    )
    manager = models.CharField(
        max_length=250,
        verbose_name='ФИО менеджера',
        blank=True,
    )
    phone = models.CharField(
        max_length=11,
        verbose_name='Телефон менеджера',
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Емейл менеджера',
        blank=True,
    )
    comments = models.TextField(
        verbose_name='Комментарии',
        blank=True,
    )
    partnership_shema = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Модель сотрудничества',
        help_text='Например: агентская схема, предоплата, скидка 30%'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
