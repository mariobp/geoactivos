# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-21 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activo',
            options={'verbose_name': 'Activo Serial', 'verbose_name_plural': 'Activos Seriales'},
        ),
        migrations.AlterModelOptions(
            name='activonoserial',
            options={'verbose_name': 'Activo no serial', 'verbose_name_plural': 'Activo no seriales'},
        ),
        migrations.AlterModelOptions(
            name='articulo',
            options={'verbose_name': 'Articulo serial', 'verbose_name_plural': 'Articulos seriales'},
        ),
        migrations.AlterModelOptions(
            name='articulonoserial',
            options={'verbose_name': 'Articulo no serial', 'verbose_name_plural': 'Aticulos no seriales'},
        ),
    ]
