# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-17 20:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180117_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anexo_orcamento',
            name='file_name',
            field=models.FileField(upload_to='orcamento/'),
        ),
    ]