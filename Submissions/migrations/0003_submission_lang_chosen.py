# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Submissions', '0002_submission_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='lang_chosen',
            field=models.CharField(default=b'cpp', max_length=10),
            preserve_default=True,
        ),
    ]
