# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='testing',
            field=models.TextField(default=b'none'),
            preserve_default=True,
        ),
    ]
