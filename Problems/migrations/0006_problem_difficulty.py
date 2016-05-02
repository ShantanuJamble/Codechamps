# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0005_auto_20150917_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(default=b'easy', max_length=8),
            preserve_default=True,
        ),
    ]
