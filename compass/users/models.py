from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from compass import settings

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    first_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name='Имя',
        validators=[
            RegexValidator(
                regex='[-a-zA-Zа-яА-Я]+',
                message='Имя может содержать только буквы')
        ]
    )
    last_name = models.CharField(
        blank=False,
        max_length=150,
        verbose_name='Фамилия',
        validators=[
            RegexValidator(
                regex='[-a-zA-Zа-яА-Я]+',
                message='Фамилия может содержать только буквы')
        ]
    )
    email = models.EmailField(
        'email address',
        max_length=settings.MAX_EMAIL_LENGTH,
        unique=True,
    )
    phone_mobile = models.CharField(
        'телефон личный',
        max_length=11,
        unique=True,
    )
    phone_work = models.CharField(  # добавить регулярку на телефон
        'телефон рабочий',
        max_length=11,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username