# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0004_auto_20150917_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='body',
            field=models.TextField(max_length=1000),
            preserve_default=True,
        ),
    ]
