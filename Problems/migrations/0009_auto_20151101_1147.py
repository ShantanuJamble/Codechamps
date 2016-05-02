# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0008_auto_20151019_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='body',
            field=models.TextField(max_length=2000),
            preserve_default=True,
        ),
    ]
