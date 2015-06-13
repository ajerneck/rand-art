# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0002_article_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='testing',
        ),
    ]
