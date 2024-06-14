from django.db import models

from tags.variables import ALLOWED_LEN_NAME


class Tag(models.Model):
    name = models.CharField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Тег',
        unique=True,
    )
    slug = models.SlugField(
        max_length=ALLOWED_LEN_NAME,
        verbose_name='Слаг тега',
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
