# Generated by Django 3.2.3 on 2024-06-18 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20240613_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='is_favorited',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='is_in_shopping_cart',
        ),
    ]
