# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-13 20:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0013_auto_20170407_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish_To_Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WTO_drug_name', models.CharField(max_length=200)),
                ('WTO_drug_brand', models.CharField(max_length=200)),
                ('WTO_drug_strength', models.CharField(max_length=50)),
                ('client_obj_WTO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
