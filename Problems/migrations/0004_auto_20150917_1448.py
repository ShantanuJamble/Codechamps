# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Problems', '0003_problem_test_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='test_counts',
            new_name='test_count',
        ),
    ]
