# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='wishes',
            field=models.ManyToManyField(related_name='wished_for', to='login.User'),
        ),
    ]
