# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-02 22:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0002_auto_20160502_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='captcha',
            name='grid_images',
            field=models.BinaryField(default=b'sdlfkj'),
            preserve_default=False,
        ),
    ]