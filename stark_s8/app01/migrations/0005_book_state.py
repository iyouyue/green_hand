# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-18 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20180318_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='state',
            field=models.IntegerField(choices=[(1, '已出版'), (2, '未出版')], default=1),
        ),
    ]
