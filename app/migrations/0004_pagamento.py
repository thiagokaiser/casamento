# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-11 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180108_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=40)),
                ('dt_pagto', models.DateField(blank=True, null=True)),
                ('dt_vencto', models.DateField(blank=True, null=True)),
                ('valor_pagto', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('valor_multa', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('valor_desconto', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Orcamento')),
            ],
        ),
    ]
