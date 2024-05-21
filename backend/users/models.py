from django.contrib.auth.models import AbstractUser
from django.db import models

from users.variables import ALLOWED_LEN_NAME, ALLOWED_LEN_EMAIL_OR_PASSWORD


class User(AbstractUser):
    first_name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=ALLOWED_LEN_EMAIL_OR_PASSWORD,
        verbose_name='Почта',
    )
    password = models.CharField(
        max_length=ALLOWED_LEN_EMAIL_OR_PASSWORD,
        verbose_name='Пароль',
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Наличие подписки',
    )
    avatar = models.ImageField(
        blank=True,
        verbose_name='Аватар',
        )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
