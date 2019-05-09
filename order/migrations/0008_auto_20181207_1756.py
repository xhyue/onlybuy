# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-12-07 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20181207_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logisticsinfo',
            name='logist',
        ),
        migrations.AddField(
            model_name='logistics',
            name='logist',
            field=models.ManyToManyField(to='order.LogisticsInfo'),
        ),
        migrations.AddField(
            model_name='logisticsinfo',
            name='order',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
            preserve_default=False,
        ),
    ]
