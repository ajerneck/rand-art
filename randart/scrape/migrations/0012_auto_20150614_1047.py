# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0011_auto_20150614_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learner', models.CharField(max_length=400)),
                ('label', models.IntegerField()),
                ('article', models.ForeignKey(to='scrape.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='results',
            name='article',
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]
