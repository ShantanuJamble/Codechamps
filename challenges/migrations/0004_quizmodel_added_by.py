# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_person_college'),
        ('challenges', '0003_auto_20160501_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='added_by',
            field=models.ForeignKey(default=1, to='person.Person'),
            preserve_default=True,
        ),
    ]
