# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-12 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0010_auto_20181112_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='headp',
            field=models.ImageField(blank=True, default='/touxiang.png', upload_to='headphoto', verbose_name='头像'),
        ),
    ]