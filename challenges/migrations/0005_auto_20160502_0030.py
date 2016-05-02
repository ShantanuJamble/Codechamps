# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_quizmodel_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='title',
            field=models.CharField(unique=True, max_length=20, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
