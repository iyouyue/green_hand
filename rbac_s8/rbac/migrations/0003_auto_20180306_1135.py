# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-06 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_userinfo_pwd'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rbac.PermissionGroup'),
        ),
    ]
