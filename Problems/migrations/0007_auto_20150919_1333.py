# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0006_problem_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='input_sample',
            field=models.TextField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='problem',
            name='output_sample',
            field=models.TextField(max_length=100),
            preserve_default=True,
        ),
    ]
