# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0006_remove_article_testing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.IntegerField(blank=True),
            preserve_default=True,
        ),
    ]
