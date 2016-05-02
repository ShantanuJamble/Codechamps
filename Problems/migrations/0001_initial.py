# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('body', models.CharField(max_length=1000)),
                ('test_counts', models.IntegerField(default=0)),
                ('input_sample', models.CharField(max_length=100)),
                ('output_sample', models.CharField(max_length=100)),
                ('domain', models.CharField(default=b'Practice', max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
