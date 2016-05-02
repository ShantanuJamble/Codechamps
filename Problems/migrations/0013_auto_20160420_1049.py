# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0012_remove_problem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='domain',
            field=models.ForeignKey(verbose_name=b'Category', blank=True, to='challenges.Category', null=True),
            preserve_default=True,
        ),
    ]
