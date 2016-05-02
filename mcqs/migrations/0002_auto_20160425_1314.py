# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitting',
            name='programs',
            field=models.CommaSeparatedIntegerField(max_length=1024, null=True, verbose_name='Programs', blank=True),
            preserve_default=True,
        ),
    ]
