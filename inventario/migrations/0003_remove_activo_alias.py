# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 04:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_auto_20160221_0407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activo',
            name='alias',
        ),
    ]