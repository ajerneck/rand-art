# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0013_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='article',
        ),
        migrations.AddField(
            model_name='rating',
            name='label',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
