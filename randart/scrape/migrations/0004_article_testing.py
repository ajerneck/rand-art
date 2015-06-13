# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0003_remove_article_testing'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='testing',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
