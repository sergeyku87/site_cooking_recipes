from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from users.variables import (
    ALLOWED_LEN_EMAIL_OR_PASSWORD,
    ALLOWED_LEN_NAME,
    UNCORRECT_NAME,
    VALIDATION_MSG_NAME,
)


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
        unique=True,
        db_index=True,
    )
    password = models.CharField(
        max_length=ALLOWED_LEN_EMAIL_OR_PASSWORD,
        verbose_name='Пароль',
    )
    avatar = models.ImageField(
        upload_to='avatars',
        blank=True,
        verbose_name='Аватар',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        if self.username == UNCORRECT_NAME:
            raise ValidationError(
                VALIDATION_MSG_NAME.format(UNCORRECT_NAME)
            )


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name='Кто',
    )
    subscriber = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='На кого подписан',
    )

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'
