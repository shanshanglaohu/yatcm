# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-21 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compounds', '0020_prescription_yongfa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herb',
            name='image_url',
            field=models.URLField(blank=True, max_length=2048),
        ),
    ]