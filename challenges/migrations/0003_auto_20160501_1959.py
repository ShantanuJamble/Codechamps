# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_quizmodel_display_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='display_picture',
            field=models.ImageField(null=True, upload_to='competitions/', blank=True),
            preserve_default=True,
        ),
    ]
