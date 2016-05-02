# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0015_problem_quiz'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='quiz',
        ),
    ]
