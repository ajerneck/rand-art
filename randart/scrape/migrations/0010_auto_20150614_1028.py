# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0009_learner_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
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
        migrations.RemoveField(
            model_name='results',
            name='article',
        ),
        migrations.RemoveField(
            model_name='results',
            name='learner',
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]
