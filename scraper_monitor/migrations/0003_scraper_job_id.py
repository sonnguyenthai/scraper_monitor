# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-12 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_monitor', '0002_auto_20160812_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='scraper',
            name='job_id',
            field=models.CharField(default=b'', max_length=150, null=True, verbose_name=b'Job ID'),
        ),
    ]