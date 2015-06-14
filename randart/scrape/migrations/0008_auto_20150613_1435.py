# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0007_auto_20150613_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
