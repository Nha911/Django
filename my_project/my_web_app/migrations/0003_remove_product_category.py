# Generated by Django 5.2.1 on 2025-05-23 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_web_app', '0002_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
