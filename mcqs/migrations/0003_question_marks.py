# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcqs', '0002_auto_20160425_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='marks',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
