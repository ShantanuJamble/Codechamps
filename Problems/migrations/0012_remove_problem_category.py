# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0011_problem_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='category',
        ),
    ]
