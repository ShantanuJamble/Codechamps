# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='display_picture',
            field=models.ImageField(upload_to='competitions/', blank=True),
            preserve_default=True,
        ),
    ]
