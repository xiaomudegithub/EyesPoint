# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-28 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='isFinished',
            field=models.BooleanField(default=False),
        ),
    ]
