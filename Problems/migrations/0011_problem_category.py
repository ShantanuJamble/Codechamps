# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0002_quizmodel_display_picture'),
        ('Problems', '0010_problem_added_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='category',
            field=models.ForeignKey(verbose_name=b'Category', blank=True, to='challenges.Category', null=True),
            preserve_default=True,
        ),
    ]
