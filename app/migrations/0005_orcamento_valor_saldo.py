# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-12 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='valor_saldo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
