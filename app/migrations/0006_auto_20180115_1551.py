# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-15 17:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_orcamento_valor_saldo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anexo_Orcamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='')),
                ('orcamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Orcamento')),
            ],
        ),
        migrations.AddField(
            model_name='pagamento',
            name='comprovante',
            field=models.FileField(blank=True, upload_to='comprovantes/'),
        ),
    ]