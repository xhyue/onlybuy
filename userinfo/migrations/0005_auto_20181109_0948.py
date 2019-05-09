# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-09 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_auto_20181107_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='headp',
            field=models.ImageField(default='', upload_to='img/head', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='昵称'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='sex',
            field=models.CharField(blank=True, choices=[(1, '男'), (0, '女')], default=1, max_length=10, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='邮箱'),
        ),
    ]
