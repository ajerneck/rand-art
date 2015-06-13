# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0004_article_testing'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='label',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
