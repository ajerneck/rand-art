# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0008_auto_20150613_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('learner', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.IntegerField()),
                ('article', models.ForeignKey(to='scrape.Article')),
                ('learner', models.ForeignKey(to='scrape.Learner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
