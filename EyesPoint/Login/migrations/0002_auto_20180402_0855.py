# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-02 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userEmail', models.CharField(max_length=100)),
                ('valCode', models.CharField(max_length=6)),
                ('timestamp', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='isVail',
        ),
        migrations.RemoveField(
            model_name='user',
            name='userPhone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='valCode',
        ),
    ]
